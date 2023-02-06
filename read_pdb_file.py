#!/usr/bin/env python3
# functions to read a PDB (Protein Data Bank) files
#-------------------------------------------------------
import os, gzip
#-------------------------------------------------------
def pdb_to_dtype(path_to_pdb_file, out_fmt = 'str', file_type = 'uncompressed'): 
    """
    parameters
    ----------
    path_to_pdb_file: str

    out_fmt: str
        specifies whether to return file contents as a string or 
        a list (each element is a separate line)
    
    returns
    -------
    str or list
	"""
    assert isinstance(path_to_pdb_file, str)       , '<path_to_pdb_file> argument was not a str type. got {}'.format(type(path_to_pdb_file))
    assert os.path.isfile(path_to_pdb_file) == True, '<path_to_pdb_file> argument was not a valid file path. got: {}'.format(path_to_pdb_file)
    assert out_fmt in ['str', 'list']              , '<out_fmt> argument was not str or list'

    if file_type == 'compressed': 
        with gzip.open(path_to_pdb_file, 'rt') as file_obj: 

            if out_fmt == 'str': 
                return file_obj.read()

            elif out_fmt == 'list': 
                return file_obj.readlines()

    elif file_type == 'uncompressed': 
        
        with open(path_to_pdb_file, 'r') as file_obj: 

            if out_fmt == 'str': 
                return file_obj.read()

            elif out_fmt == 'list': 
                return file_obj.readlines()