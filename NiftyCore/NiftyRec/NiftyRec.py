
# NiftyRec - Tomographic Reconstruction routines 
# Stefano Pedemonte
# Center for Medical Image Computing (CMIC), University College Lonson (UCL)
# 2009-2012, London
# Aalto University, School of Science
# Summer 2013, Helsinki
# Martinos Center for Biomedical Imaging, Harvard University/MGH
# Dec. 2013, Boston

from simplewrap import *

__all__ = ['PET_project','PET_backproject','PET_project_compressed','PET_backproject_compressed','SPECT_project_parallelholes','SPECT_backproject_parallelholes','CT_project_conebeam','CT_backproject_conebeam','CT_project_parallelbeam','CT_backproject_parallelbeam'] 
niftyrec_lib_paths = [filepath(__file__), '/usr/local/niftyrec/lib/', 'C:/Prorgam Files/NiftyRec/lib/'] 

####################################### Error handling: ########################################
class ErrorInCFunction(Exception): 
    def __init__(self,msg,status,function_name): 
        self.msg = str(msg) 
        self.status = status
        self.function_name = function_name
        if self.status == status_io_error(): 
            self.status_msg = "IO Error"
        elif self.status == status_decode_error(): 
            self.status_msg = "Error Decoding file content"
        elif self.status == status_initialisation_error(): 
            self.status_msg = "Error with the initialisation of the C library"
        elif self.status == status_parameter_error(): 
            self.status_msg = "One or more of the specified parameters are not right"
        elif self.status == status_unhandled_error(): 
            self.status_msg = "Unhandled error, likely a bug. "
        else: 
            self.status_msg = "Unspecified Error"
    def __str__(self): 
        return "'%s' returned by the C Function '%s'. %s"%(self.status_msg,self.function_name,self.msg)


def status_success(): 
    """Returns the value returned by the function calls to the library in case of success. """
    r = call_c_function( niftyrec_c.status_success, [{'name':'return_value',  'type':'int', 'value':None}] ) 
    return r.return_value

def status_io_error(): 
    """Returns the integer value returned by the function calls to the library in case of IO error. """
    r = call_c_function( niftyrec_c.status_io_error, [{'name':'return_value',  'type':'int', 'value':None}] ) 
    return r.return_value

def status_decode_error(): 
    """Returns the value returned by the function calls to the library in case of error decoding a file. """
    r = call_c_function( niftyrec_c.status_decode_error, [{'name':'return_value',  'type':'int', 'value':None}] ) 
    return r.return_value

def status_initialisation_error(): 
    """Returns the value returned by the function calls to the library in case of initialisation error. """
    r = call_c_function( niftyrec_c.status_initialisation_error, [{'name':'return_value',  'type':'int', 'value':None}] ) 
    return r.return_value

def status_parameter_error(): 
    """Returns the value returned by the function calls to the library in case of parameter error. """
    r = call_c_function( niftyrec_c.status_parameter_error, [{'name':'return_value',  'type':'int', 'value':None}] ) 
    return r.return_value

def status_unhandled_error(): 
    """Returns the value returned by the function calls to the library in case of unhandled error. """
    r = call_c_function( niftyrec_c.status_unhandled_error, [{'name':'return_value',  'type':'int', 'value':None}] ) 
    return r.return_value



####################################### Load library: ########################################
def test_library_niftyrec_c(): 
    """Test whether the C library niftyrec_c responds. """
    number = 101 # just a number
    descriptor = [  {'name':'input',  'type':'int', 'value':number},
                    {'name':'output', 'type':'int', 'value':None },  ]
    r = call_c_function( niftyrec_c.echo, descriptor ) 
    return r.output == number
    
def find_c_library(path='/'): 
    global niftyrec_c
    paths = niftyrec_lib_paths+[path,] 
    for path in paths: 
        try: 
            niftyrec_c = load_c_library("niftyrec_c",path)
        except: 
            pass 
        else: 
            return True 
    return False 

niftyrec_c = None 
find_c_library() 



#################################### Create interface to the C functions: ####################################

def PET_project(activity,attenuation,binning,use_gpu=0): #FIXME: in this and all other functions, replace 'binning' object with (only the required) raw variables 
    """PET projection; output projection data is compressed. """
    descriptor = [    ] 
    r = call_c_function( niftyrec_c.PET_project, descriptor ) 
    if not r.status == petlink.status_success(): 
        raise ErrorInCFunction("The execution of 'PET_project' was unsuccessful.",r.status,'niftyrec_c.PET_project')
    return r.dictionary["projection"]


def PET_backproject(projection_data,attenuation,binning,use_gpu=0): 
    """PET back-projection; input projection data is compressed. """
    descriptor = [    ] 
    r = call_c_function( niftyrec_c.PET_backproject, descriptor ) 
    if not r.status == petlink.status_success(): 
        raise ErrorInCFunction("The execution of 'PET_backproject' was unsuccessful.",r.status,'niftyrec_c.PET_backproject')
    return r.dictionary 

    
def PET_project_compressed(activity,attenuation,offsets,locations,binning,use_gpu=0): 
    """PET projection; output projection data is compressed. """
    return 0
    descriptor = [    ] 
    r = call_c_function( niftyrec_c.PET_project_compressed, descriptor ) 
    if not r.status == petlink.status_success(): 
        raise ErrorInCFunction("The execution of 'PET_project_compressed' was unsuccessful.",r.status,'niftyrec_c.PET_project_compressed')
    return r.dictionary["projection"]


def PET_backproject_compressed(projection_data,offsets,locations,attenuation,binning,use_gpu=0): 
    """PET back-projection; input projection data is compressed. """
    return 0    
    descriptor = [    ] 
    r = call_c_function( niftyrec_c.PET_backproject_compressed, descriptor ) 
    if not r.status == petlink.status_success(): 
        raise ErrorInCFunction("The execution of 'PET_backproject_compressed' was unsuccessful.",r.status,'niftyrec_c.PET_backproject_compressed')
    return r.dictionary 


def SPECT_project_parallelholes(activity,attenuation,camera_trajectory,PSF,use_gpu=0): 
    """SPECT projection; parallel-holes geometry. """
    descriptor = [    ] 
    r = call_c_function( niftyrec_c.SPECT_project_parallelholes, descriptor ) 
    if not r.status == petlink.status_success(): 
        raise ErrorInCFunction("The execution of 'SPECT_project_parallelholes' was unsuccessful.",r.status,'niftyrec_c.SPECT_project_parallelholes')
    return r.dictionary


def SPECT_backproject_parallelholes(projection_data,attenuation,camera_trajectory,PSF,use_gpu=0): 
    """SPECT back-projection; parallel-holes geometry. """
    descriptor = [    ] 
    r = call_c_function( niftyrec_c.SPECT_backproject_parallelholes, descriptor ) 
    if not r.status == petlink.status_success(): 
        raise ErrorInCFunction("The execution of 'SPECT_backproject_parallelholes' was unsuccessful.",r.status,'niftyrec_c.SPECT_backproject_parallelholes')
    return r.dictionary 


def CT_project_conebeam(attenuation,camera_trajectory,source_trajectory,use_gpu=0): 
    """Transmission imaging projection; cone-beam geometry. """
    descriptor = [    ] 
    r = call_c_function( niftyrec_c.CT_project_conebeam, descriptor ) 
    if not r.status == petlink.status_success(): 
        raise ErrorInCFunction("The execution of 'CT_project_conebeam' was unsuccessful.",r.status,'niftyrec_c.CT_project_conebeam')
    return r.dictionary     


def CT_backproject_conebeam(projection_data,camera_trajectory,source_trajectory,use_gpu=0): 
    """Transmission imaging back-projection; cone-beam geometry. """
    descriptor = [    ] 
    r = call_c_function( niftyrec_c.CT_backproject_conebeam, descriptor ) 
    if not r.status == petlink.status_success(): 
        raise ErrorInCFunction("The execution of 'CT_backproject_conebeam' was unsuccessful.",r.status,'niftyrec_c.CT_backproject_conebeam')
    return r.dictionary             


def CT_project_parallelbeam(attenuation,camera_trajectory,source_trajectory,use_gpu=0): 
    """Transmission imaging projection; parallel-beam geometry. """
    descriptor = [    ] 
    r = call_c_function( niftyrec_c.CT_project_parallelbeam, descriptor ) 
    if not r.status == petlink.status_success(): 
        raise ErrorInCFunction("The execution of 'CT_project_parallelbeam' was unsuccessful.",r.status,'niftyrec_c.CT_project_parallelbeam')
    return r.dictionary         


def CT_backproject_parallelbeam(attenuation,camera_trajectory,source_trajectory,use_gpu=0): 
    """Transmission imaging back-projection; parallel-beam geometry. """
    descriptor = [    ] 
    r = call_c_function( niftyrec_c.CT_backproject_parallelbeam, descriptor ) 
    if not r.status == petlink.status_success(): 
        raise ErrorInCFunction("The execution of 'CT_backproject_parallelbeam' was unsuccessful.",r.status,'niftyrec_c.CT_backproject_parallelbeam')
    return r.dictionary         


