rule all:
    input:
        expand("result/clean_data/{sample}_1.fastp.fq.gz", sample=SAMPLES),
        expand("result/clean_data/{sample}_2.fastp.fq.gz", sample=SAMPLES),
        expand("result/megahit/{sample}_megahit", sample=SAMPLES),
        expand("result/megahit/{sample}_final.contigs.fa", sample=SAMPLES),
        expand("result/megahit/{sample}_final.contigs.filter.fa", sample=SAMPLES),
        expand("result/megahit/{sample}_final.contigs.filter.blastnr.m8", sample=SAMPLES),
        expand("{sample}_final.contigs_300_blastnr_twocol.m8", sample=SAMPLES),
        expand("{sample}_final.contigs_300_blastnr_twocol_virus.m8", sample=SAMPLES),
        expand("{sample}_final.contigs_300_blastnr_twocol_virus_seqid.m8", sample=SAMPLES),
        expand("{sample}_final.contigs_300_blastnr_twocol_virus_seqid.fasta", sample=SAMPLES),
        expand("{sample}_final.contigs_300_blastnr_twocol_virus_seq_blastnt.m8", sample=SAMPLES),
        expand("{sample}_final.contigs_300_blastnr_twocol_virus_seq_blastnt_twocol.m8", sample=SAMPLES),
        expand("{sample}_final.contigs_300_blastnr_twocol_virus_seq_blastnt_twocol_redup.m8", sample=SAMPLES),
        expand("{sample}_final.contigs_300_blastnr_twocol_virus_seq_blastnt_twocol_redup_virus.m8", sample=SAMPLES),
        expand("{sample}_final.contigs_300_blastnr_twocol_virus_seq_blastnt_twocol_redup-firstcol.m8", sample=SAMPLES),
        expand("{sample}_final.contigs_300_blastnr_twocol_virus_seqid_second.m8", sample=SAMPLES),
        expand("{sample}_unblast_nt_seqid", sample=SAMPLES),
        expand("{sample}_final.contigs_300_blastnr_twocol_virus_seq_blastnt_twocol_redup_virus_secol.m8", sample=SAMPLES),
        expand("{sample}_potential_virus_seqid", sample=SAMPLES),
        expand("{sample}_potential_virus_seqid_taxid", sample=SAMPLES),
        expand("{sample}_potential_virus_seqid_taxid_annotation", sample=SAMPLES),
        expand("{sample}_potential_virus_seqid_taxid_annotation_statistic", sample=SAMPLES)

# fastp quality control
rule run_fastp:
    input:
        r1='rawdata/{sample}_1.fq.gz',
        r2='rawdata/{sample}_2.fq.gz'
    output:
        r1='result/clean_data/{sample}_1.fastp.fq.gz',
        r2='result/clean_data/{sample}_2.fastp.fq.gz',
        report='result/clean_data/{sample}.fastp.html',
        json='result/clean_data/{sample}.fastp.json'
    threads: 10
    log: "result/clean_data/{sample}.fastp.log"
    shell:
        """
        fastp -w {threads} -i {input.r1} -I {input.r2} \
              -o {output.r1} -O {output.r2} \
              -h {output.report} -j {output.json} \
              1>{log} 2>&1
        """

# megahit assembly
rule run_megahit:
    input:
        r1='result/clean_data/{sample}_1.fastp.fq.gz',
        r2='result/clean_data/{sample}_2.fastp.fq.gz'
    output:
        directory("result/megahit/{sample}_megahit")
    log: "result/megahit/{sample}_megahit.log"
    shell:
        "megahit -t 60 -o {output} -1 {input.r1} -2 {input.r2} 1>{log} 2>&1"

# Extract final.contigs.fa and rename
rule final_contig_extren:
    input:
        folder="result/megahit/{sample}_megahit"
    output:
        newfile="result/megahit/{sample}_final.contigs.fa"
    shell:
        "python script/final_contig_extren.py {input.folder} {output.newfile}"

# Filter sequences by length
rule filter_contigs_by_length:
    input:
        contigs="result/megahit/{sample}_final.contigs.fa"
    output:
        filtered="result/megahit/{sample}_final.contigs.filter.fa"
    log:
        "result/megahit/{sample}_filter.log"
    shell:
        "python script/filter_fasta.py {input.contigs} {output.filtered} 300 1>{log} 2>&1"

# BLASTx against NR database
rule blastx_against_nr:
    input:
        "result/megahit/{sample}_final.contigs.filter.fa"
    output:
        "result/megahit/{sample}_final.contigs.filter.blastnr.m8"
    params:
        nr_db="/icdc/Database/NR_2023_12.dmnd",
        evalue=1e-5
    log:
        "result/megahit/{sample}_blastnr.log"
    shell:
        "diamond blastx --query {input} "
        "--out {output} "
        "--outfmt 6 "
        "--db /icdc/Database/NR_2023_12.dmnd "
        "--evalue 1e-5 "
        "-k 1 1>{log} 2>&1"

# Keep the first two columns
rule keep_first_two_columns:
    input:
        "result/megahit/{sample}_final.contigs.filter.blastnr.m8"
    output:
        "{sample}_final.contigs_300_blastnr_twocol.m8"
    shell:
        "python script/keep_first_two_columns.py {input} {output}"

# Match NR database virus sequences (filter for virus sequences)
rule merge_files:
    input:
        i1="{sample}_final.contigs_300_blastnr_twocol.m8",
        i2="database/nr_virus.txt"
    output:
        "{sample}_final.contigs_300_blastnr_twocol_virus.m8"
    shell:
        "python script/merge_files_endfirst.py {input.i1} {input.i2} {output}"

# Extract the second column
rule extract_second_column:
    input:
        "{sample}_final.contigs_300_blastnr_twocol_virus.m8"
    output:
        "{sample}_final.contigs_300_blastnr_twocol_virus_seqid.m8"
    shell:
        "awk '{{print $2}}' {input} > {output}"

# Filter original sequences using sequence IDs and output as FASTA
rule grep_sequences:
    input:
        seqid="{sample}_final.contigs_300_blastnr_twocol_virus_seqid.m8",
        fasta="result/megahit/{sample}_final.contigs.filter.fa"
    output:
        "{sample}_final.contigs_300_blastnr_twocol_virus_seqid.fasta"
    shell:
        "seqkit grep --pattern-file {input.seqid} {input.fasta} > {output}"

# Run BLASTn
rule run_blastn:
    input:
        "{sample}_final.contigs_300_blastnr_twocol_virus_seqid.fasta"
    output:
        "{sample}_final.contigs_300_blastnr_twocol_virus_seq_blastnt.m8"
    params:
        db="/icdc/Database/NT_db/NT_2023_12",
        max_target_seqs=1,
        num_threads=64,
        outfmt=6
    shell:
        "blastn -query {input} -db {params.db} -max_target_seqs {params.max_target_seqs} -num_threads {params.num_threads} -outfmt {params.outfmt} -out {output}"

# Keep first two columns from BLASTn
rule keep_first_two_columns_blastnt:
    input:
        "{sample}_final.contigs_300_blastnr_twocol_virus_seq_blastnt.m8"
    output:
        "{sample}_final.contigs_300_blastnr_twocol_virus_seq_blastnt_twocol.m8"
    shell:
        """
        if [ -s {input} ]; then
            python script/keep_first_two_columns.py {input} {output}
        else
            touch {output}
        fi
        """

# Remove duplicates
rule remove_duplicates:
    input:
        "{sample}_final.contigs_300_blastnr_twocol_virus_seq_blastnt_twocol.m8"
    output:
        "{sample}_final.contigs_300_blastnr_twocol_virus_seq_blastnt_twocol_redup.m8"
    shell:
        """
        if [ -s {input} ]; then
            python script/remove_duplicates.py {input} {output}
        else
            touch {output}
        fi
        """

# Match filtered BLASTn results with NT virus database
rule merge_files_blastnt_redup:
    input:
        i3="{sample}_final.contigs_300_blastnr_twocol_virus_seq_blastnt_twocol_redup.m8",
        i4="database/nt_virus.txt"
    output:
        "{sample}_final.contigs_300_blastnr_twocol_virus_seq_blastnt_twocol_redup_virus.m8"
    shell:
        """
        if [ -s {input.i3} ]; then
            python script/merge_files_endfirst.py {input.i3} {input.i4} {output}
        else
            touch {output}
        fi
        """

# Extract first column
rule extract_first_column:
    input:
        "{sample}_final.contigs_300_blastnr_twocol_virus_seq_blastnt_twocol_redup.m8"
    output:
        "{sample}_final.contigs_300_blastnr_twocol_virus_seq_blastnt_twocol_redup-firstcol.m8"
    shell:
        "awk '{{print $1}}' {input} > {output}"

# Extract second column using script
rule extract_second_column_script:
    input:
        "{sample}_final.contigs_300_blastnr_twocol_virus.m8"
    output:
        "{sample}_final.contigs_300_blastnr_twocol_virus_seqid_second.m8"
    shell:
        "python script/extract_second_column.py {input} {output}"

# Find sequence IDs present in the first list but not in the second
rule find_difference:
    input:
        first_col_file="{sample}_final.contigs_300_blastnr_twocol_virus_seq_blastnt_twocol_redup-firstcol.m8",
        second_col_file="{sample}_final.contigs_300_blastnr_twocol_virus_seqid_second.m8"
    output:
        "{sample}_unblast_nt_seqid"
    shell:
        "python script/find_difference.py {input.first_col_file} {input.second_col_file} {output}"

# Extract second column from reduped virus BLASTn results
rule extract_second_column_blastnt_redup_virus:
    input:
        "{sample}_final.contigs_300_blastnr_twocol_virus_seq_blastnt_twocol_redup_virus.m8"
    output:
        "{sample}_final.contigs_300_blastnr_twocol_virus_seq_blastnt_twocol_redup_virus_secol.m8"
    shell:
        "python script/extract_second_column.py {input} {output}"

# Concatenate two files to create list of potential viral sequence IDs
rule concat_potential_virus_seqids:
    input:
        unblast_nt_seqid="{sample}_unblast_nt_seqid",
        blastnt_redup_virus_secol="{sample}_final.contigs_300_blastnr_twocol_virus_seq_blastnt_twocol_redup_virus_secol.m8"
    output:
        "{sample}_potential_virus_seqid"
    shell:
        "cat {input.unblast_nt_seqid} {input.blastnt_redup_virus_secol} > {output}"

# Extract rows from BLAST result by virus sequence ID
rule extract_rows_by_seqid:
    input:
        seqid_file="{sample}_potential_virus_seqid",
        blast_results="{sample}_final.contigs_300_blastnr_twocol_virus.m8"
    output:
        "{sample}_potential_virus_seqid_taxid"
    shell:
        "python script/extract_rows.py {input.seqid_file} {input.blast_results} {output}"

# Merge potential viral sequence IDs with taxonomy annotation
rule merge_potential_virus_taxid_annotation:
    input:
        taxid_file="{sample}_potential_virus_seqid_taxid",
        annotation_file="database/NCBI_Main.taxid_new.txt"
    output:
        "{sample}_potential_virus_seqid_taxid_annotation"
    shell:
        "python script/merge_files_endfirst.py {input.taxid_file} {input.annotation_file} {output}"

# Summarize 12th column from annotation
rule summarize_12th_column:
    input:
        "{sample}_potential_virus_seqid_taxid_annotation"
    output:
        "{sample}_potential_virus_seqid_taxid_annotation_statistic"
    shell:
        "awk '{{print $12}}' {input} | sort | uniq -c > {output}"
