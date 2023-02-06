#!/usr/bin/env python3
# functions to extract protein features from PDB (Protein Data Bank) files
#-------------------------------------------------------
import sys, os, pandas as pd
from read_pdb_file import pdb_to_dtype
#-------------------------------------------------------
def get_afdb_disorder_vals(path_to_pdb_file, verbose = 0): 
    """outputs scores for the predicted disorder for each amino acid
    in a protein. 
    
    note
     The expected required data is a PDB file from AFDB (alphafold database).
     In these PDB files,  the bfactor (aka temperature factor) column specifies 
     scores for the protein structure predictions (PLDD). This data is used to score
     disorder per amino acid (see https://doi.org/10.3390/ijms23094591 for more info)

    returns
    -------
    DataFrame that specifies amino acid sequences, their ids and PLDD and tPLD values. 
    """

    # read pdb file as a string
    pdb_file_lines = pdb_to_dtype(path_to_pdb_file, out_fmt = 'list')
    if verbose == 1: 
        print('lines in pdb file: {}'.format(len(pdb_file_lines)))

    # extract aa sequences
    aa_seq          = get_aaseq_from_seqres(pdb_file_lines, verbose = verbose)

    # extract bfactor values (for AFDB - these are confidence scores of the structure prediction)
    bf_to_seqres_id = get_bfactor_from_atom(pdb_file_lines, verbose = verbose)

    # map amino acids and their ids to bfactor values
    aa_and_bfactor_df = pd.DataFrame.from_dict(bf_to_seqres_id, orient = 'index', columns = ['PLDD']).rename_axis('AA_id', axis = 1).astype(float)
    
    aa_and_bfactor_df['AA']   = aa_seq
    aa_and_bfactor_df['tPLD'] = 1 - (aa_and_bfactor_df['PLDD']/100)

    aa_and_bfactor_info       = aa_and_bfactor_df[['AA', 'PLDD', 'tPLD']].copy()

    return aa_and_bfactor_info
#-------------------------------------------------------
def get_bfactor_from_atom(pdb_file_str, verbose = 1): 
    """maps b-factor values to seqres ids. Uses data 
    from ATOM record type"""

    atom_rows = [i for i in pdb_file_str if i.startswith('ATOM')]
    if verbose == 1:
        print('number of ATOM rows: {}'.format(len(atom_rows)))

    res_id_and_bfactor = []

    for row in atom_rows: 
        row_info = row.split()
        res_id, bfactor = row_info[5], row_info[-2]

        res_id_and_bfactor.append((res_id, bfactor))

    dict_res_id_and_bfactor = dict(res_id_and_bfactor)
    if verbose == 1:
        print('number of ids: {}'.format(len(dict_res_id_and_bfactor)))

    return dict_res_id_and_bfactor
#-------------------------------------------------------
def get_aaseq_from_seqres(pdb_file_str, verbose = 1): 
    """extracts an amino acid sequence from SEQRES record type"""

    seqres_rows = [i for i in pdb_file_str if i.startswith('SEQRES')]
    if verbose == 1:
        print('number of SEQRES rows: {}'.format(len(seqres_rows)))

    aa_seq = []
    for row in seqres_rows: 
        aa_seq += row.split()[4:]
        
    assert len(aa_seq) == int(seqres_rows[0].split()[3]), 'number of amino acids did not match expected number'
    if verbose == 1:
        print('number of amino acids did matched the expected number')

    return aa_seq