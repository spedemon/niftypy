# NiftyCore - Medical imaging tools
# Stefano Pedemonte
# Center for Medical Image Computing (CMIC), University College Lonson (UCL)
# 2009-2012, London
# Aalto University, School of Science
# Summer 2013, Helsinki
# Martinos Center for Biomedical Imaging, Harvard University/MGH
# Jan. 2014, Boston

from simplewrap import *
import numpy


__all__ = ['niftyreg_c','test_library_niftyreg_c','resample_image_rigid','deriv_intensity_wrt_space_rigid','deriv_intensity_wrt_transformation_rigid','deriv_ssd_wrt_transformation_rigid','gaussian_smoothing',]

library_name = "_reg_array_interface"
niftyreg_lib_paths = [filepath(__file__), './', '/usr/local/niftyrec/lib/', 'C:/Prorgam Files/NiftyRec/lib/','/Users/spedemon/Desktop/NiftyRec-1.6.9/NiftyRec_install/lib/'] 


####################################### Error handling: ########################################

class ErrorInCFunction(Exception): 
    def __init__(self,msg,status,function_name): 
        self.msg = str(msg) 
        self.status = status
        self.function_name = function_name
        if self.status == status_io_error(): 
            self.status_msg = "IO Error"
        elif self.status == status_initialisation_error(): 
            self.status_msg = "Error with the initialisation of the C library"
        elif self.status == status_parameter_error(): 
            self.status_msg = "One or more of the specified parameters are not right"
        elif self.status == status_unhandled_error(): 
            self.status_msg = "Unhandled error, likely a bug. "
        else: 
            self.status_msg = "Unspecified Error"
    def __str__(self): 
        return "'%s' returned by the C Function '%s' (error code %d). %s"%(self.status_msg,self.function_name,self.status,self.msg)


def status_success(): 
    """Returns the value returned by the function calls to the library in case of success. """
    r = call_c_function( niftyreg_c.status_success, [{'name':'return_value',  'type':'uint', 'value':None}] ) 
    return r.return_value

def status_io_error(): 
    """Returns the integer value returned by the function calls to the library in case of IO error. """
    r = call_c_function( niftyreg_c.status_io_error, [{'name':'return_value',  'type':'uint', 'value':None}] ) 
    return r.return_value

def status_initialisation_error(): 
    """Returns the value returned by the function calls to the library in case of initialisation error. """
    r = call_c_function( niftyreg_c.status_initialisation_error, [{'name':'return_value',  'type':'uint', 'value':None}] ) 
    return r.return_value

def status_parameter_error(): 
    """Returns the value returned by the function calls to the library in case of parameter error. """
    r = call_c_function( niftyreg_c.status_parameter_error, [{'name':'return_value',  'type':'uint', 'value':None}] ) 
    return r.return_value

def status_unhandled_error(): 
    """Returns the value returned by the function calls to the library in case of unhandled error. """
    r = call_c_function( niftyreg_c.status_unhandled_error, [{'name':'return_value',  'type':'uint', 'value':None}] ) 
    return r.return_value



####################################### Load library: ########################################
def test_library_niftyreg_c(): 
    """Test whether the C library niftyreg_c responds. """
    number = 101 # just a number
    descriptor = [  {'name':'input',  'type':'int', 'value':number},
                    {'name':'output', 'type':'int', 'value':None },  ]
    r = call_c_function( niftyreg_c.echo, descriptor ) 
    return r.output == number
    

(found,fullpath,path) = find_c_library(library_name,niftyreg_lib_paths) 
if found == NOT_FOUND: 
    raise LibraryNotFound("niftyreg")
elif found == FOUND_NOT_LOADABLE: 
    print "The library %s cannot be loaded, please make sure that the path has been exported. "%fullpath
    print "1) Before launching Python, type the following in the terminal (the same terminal): "
    import platform
    if platform.system()=='Linux':
        print "export LD_LIBRARY_PATH=%s"%path
    elif platform.system()=='Darwin':
        print "export DYLD_LIBRARY_PATH=%s"%path
    elif platform.system()=='Windows':
        print "Add %s to the system PATH using Control Panel -> Advanced Settings -> System -> .."%path
else: 
    niftyreg_c = load_c_library(fullpath)


#################################### Create interface to the C functions: ####################################




def resample_image_rigid(image_data,translation,rotation,center_rotation,sform=None,use_gpu=1): 
    """Resample a 3D image according to rigid transformation parameters. """
    if sform==None: 
        sform=numpy.eye(4,dtype=float32) 
    descriptor = [{'name':'image_data',          'type':'array',  'value':image_data,                'dtype':float32}, 
                  {'name':'resampled_image_data','type':'array',  'value':None,                      'dtype':float32,   'size':(image_data.shape),   'order':"F"    }, 
                  {'name':'size_x',              'type':'uint',   'value':image_data.shape[0]}, 
                  {'name':'size_y',              'type':'uint',   'value':image_data.shape[1]}, 
                  {'name':'size_z',              'type':'uint',   'value':image_data.shape[2]}, 
                  {'name':'translation',         'type':'array',  'value':translation,               'dtype':float32 },
                  {'name':'rotation',            'type':'array',  'value':rotation,                  'dtype':float32 },
                  {'name':'center_rotation',     'type':'array',  'value':center_rotation,           'dtype':float32 },
                  {'name':'sform',               'type':'array',  'value':sform,                     'dtype':float32 }, 
                  {'name':'use_gpu',             'type':'int',    'value':numpy.uint32(use_gpu)}, ]
    r = call_c_function( niftyreg_c.REG_array_resample_image_rigid, descriptor ) 
    if not r.status == status_success(): 
        raise ErrorInCFunction("The execution of 'REG_array_resample_image_rigid' was unsuccessful.",r.status,'niftyreg_c.REG_array_resample_image_rigid')
    return r.dictionary['resampled_image_data']



def deriv_intensity_wrt_space_rigid(image_data,translation,rotation,center_rotation,sform=None,use_gpu=1): 
    """Compute the spatial gradient of a 3D image, after transforming it according to rigid transformation parameters. """
    if sform==None: 
        sform=numpy.eye(4,dtype=float32) 
    descriptor = [{'name':'image_data',          'type':'array',  'value':image_data,                'dtype':float32}, 
                  {'name':'gradient',            'type':'array',  'value':None,                      'dtype':float32,   'size':(image_data.shape[0],image_data.shape[1],image_data.shape[2],3),   'order':"F"    }, 
                  {'name':'size_x',              'type':'uint',   'value':image_data.shape[0]}, 
                  {'name':'size_y',              'type':'uint',   'value':image_data.shape[1]}, 
                  {'name':'size_z',              'type':'uint',   'value':image_data.shape[2]}, 
                  {'name':'translation',         'type':'array',  'value':translation,               'dtype':float32 },
                  {'name':'rotation',            'type':'array',  'value':rotation,                  'dtype':float32 },
                  {'name':'center_rotation',     'type':'array',  'value':center_rotation,           'dtype':float32 },
                  {'name':'sform',               'type':'array',  'value':sform,                     'dtype':float32 }, 
                  {'name':'use_gpu',             'type':'int',    'value':numpy.uint32(use_gpu)}, ]
    r = call_c_function( niftyreg_c.REG_array_d_intensity_d_space_rigid, descriptor ) 
    if not r.status == status_success(): 
        raise ErrorInCFunction("The execution of 'REG_array_d_intensity_d_space_rigid' was unsuccessful.",r.status,'niftyreg_c.REG_array_d_intensity_d_space_rigid')
    return r.dictionary['gradient']



def deriv_intensity_wrt_transformation_rigid(image_data,translation,rotation,center_rotation,sform=None,use_gpu=1): 
    """Compute the spatial gradient of a 3D image, after transforming it according to rigid transformation parameters. """
    if sform==None: 
        sform=numpy.eye(4,dtype=float32) 
    descriptor = [{'name':'image_data',          'type':'array',  'value':image_data,                'dtype':float32}, 
                  {'name':'gradient',            'type':'array',  'value':None,                      'dtype':float32,   'size':(image_data.shape[0],image_data.shape[1],image_data.shape[2],6),   'order':"F"    }, 
                  {'name':'size_x',              'type':'uint',   'value':image_data.shape[0]}, 
                  {'name':'size_y',              'type':'uint',   'value':image_data.shape[1]}, 
                  {'name':'size_z',              'type':'uint',   'value':image_data.shape[2]}, 
                  {'name':'translation',         'type':'array',  'value':translation,               'dtype':float32 },
                  {'name':'rotation',            'type':'array',  'value':rotation,                  'dtype':float32 },
                  {'name':'center_rotation',     'type':'array',  'value':center_rotation,           'dtype':float32 },
                  {'name':'sform',               'type':'array',  'value':sform,                     'dtype':float32 }, 
                  {'name':'use_gpu',             'type':'int',    'value':numpy.uint32(use_gpu)}, ]
    r = call_c_function( niftyreg_c.REG_array_d_intensity_d_transformation_rigid, descriptor ) 
    if not r.status == status_success(): 
        raise ErrorInCFunction("The execution of 'REG_array_d_intensity_d_transformation_rigid' was unsuccessful.",r.status,'niftyreg_c.REG_array_d_intensity_d_transformation_rigid')
    return r.dictionary['gradient']




def deriv_ssd_wrt_transformation_rigid():
    pass 



def gaussian_smoothing(image_data): 
    pass 


