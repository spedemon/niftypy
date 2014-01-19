
# NiftyRec - Ra-tracing tools
# Stefano Pedemonte
# Center for Medical Image Computing (CMIC), University College Lonson (UCL)
# 2009-2012, London
# Aalto University, School of Science
# Summer 2013, Helsinki
# Martinos Center for Biomedical Imaging, Harvard University/MGH
# Dec. 2013, Boston

from simplewrap import *
import numpy


__all__ = ['test_library_niftyrec_c',
'PET_project','PET_backproject','PET_project_compressed','PET_backproject_compressed',
'SPECT_project_parallelholes','SPECT_backproject_parallelholes',
'CT_project_conebeam','CT_backproject_conebeam','CT_project_parallelbeam','CT_backproject_parallelbeam',
'ET_spherical_phantom','ET_cylindrical_phantom','ET_spheres_ring_phantom'] 

library_name = "_et_array_interface"
niftyrec_lib_paths = [filepath(__file__), './', '/usr/local/niftyrec/lib/', 'C:/Prorgam Files/NiftyRec/lib/','/Users/spedemon/Desktop/NiftyRec-1.6.9/NiftyRec_install/lib/'] 




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
        return "'%s' returned by the C Function '%s'. %s"%(self.status_msg,self.function_name,self.msg)


def status_success(): 
    """Returns the value returned by the function calls to the library in case of success. """
    r = call_c_function( niftyrec_c.status_success, [{'name':'return_value',  'type':'uint', 'value':None}] ) 
    return r.return_value

def status_io_error(): 
    """Returns the integer value returned by the function calls to the library in case of IO error. """
    r = call_c_function( niftyrec_c.status_io_error, [{'name':'return_value',  'type':'uint', 'value':None}] ) 
    return r.return_value

def status_initialisation_error(): 
    """Returns the value returned by the function calls to the library in case of initialisation error. """
    r = call_c_function( niftyrec_c.status_initialisation_error, [{'name':'return_value',  'type':'uint', 'value':None}] ) 
    return r.return_value

def status_parameter_error(): 
    """Returns the value returned by the function calls to the library in case of parameter error. """
    r = call_c_function( niftyrec_c.status_parameter_error, [{'name':'return_value',  'type':'uint', 'value':None}] ) 
    return r.return_value

def status_unhandled_error(): 
    """Returns the value returned by the function calls to the library in case of unhandled error. """
    r = call_c_function( niftyrec_c.status_unhandled_error, [{'name':'return_value',  'type':'uint', 'value':None}] ) 
    return r.return_value



####################################### Load library: ########################################
def test_library_niftyrec_c(): 
    """Test whether the C library niftyrec_c responds. """
    number = 101 # just a number
    descriptor = [  {'name':'input',  'type':'int', 'value':number},
                    {'name':'output', 'type':'int', 'value':None },  ]
    r = call_c_function( niftyrec_c.echo, descriptor ) 
    return r.output == number
    

(found,fullpath,path) = find_c_library(library_name,niftyrec_lib_paths) 
if found == NOT_FOUND: 
    raise LibraryNotFound("NiftyRec")
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
    #Exporting path now does not work, what can be done at this point to handle gracefully the missing environment variable?  
    #export_dl_library_path(path) 
    #niftyrec_c = load_c_library(fullpath) 
else: 
    niftyrec_c = load_c_library(fullpath)

#################################### Create interface to the C functions: ####################################

def PET_project(activity,attenuation,binning,use_gpu=0): #FIXME: in this and all other functions, replace 'binning' object with (only the required) raw variables 
    """PET projection; output projection data is compressed. """
    descriptor = [{'name':'activity',            'type':'array',  'value':activity}, 
                  {'name':'activity_size_x',     'type':'int',    'value':activity.shape[0]}, 
                  {'name':'activity_size_y',     'type':'int',    'value':activity.shape[1]}, 
                  {'name':'activity_size_z',     'type':'int',    'value':activity.shape[2]}, 

                  {'name':'attenuation',         'type':'array',  'value':attenuation}, 
                  {'name':'attenuation_size_x',  'type':'int',    'value':attenuation.shape[0]}, 
                  {'name':'attenuation_size_y',  'type':'int',    'value':attenuation.shape[1]}, 
                  {'name':'attenuation_size_z',  'type':'int',    'value':attenuation.shape[2]}, 

                  {'name':'use_gpu',             'type':'int',    'value':use_gpu}, ]
    r = call_c_function( niftyrec_c.PET_project, descriptor ) 
    if not r.status == status_success(): 
        raise ErrorInCFunction("The execution of 'PET_project' was unsuccessful.",r.status,'niftyrec_c.PET_project')
    return r.dictionary['projection']


def PET_backproject(projection_data,attenuation,binning,use_gpu=0): 
    """PET back-projection; input projection data is compressed. """
    descriptor = [    ] 
    r = call_c_function( niftyrec_c.PET_backproject, descriptor ) 
    if not r.status == status_success(): 
        raise ErrorInCFunction("The execution of 'PET_backproject' was unsuccessful.",r.status,'niftyrec_c.PET_backproject')
    return r.dictionary 

    
def PET_project_compressed(activity, attenuation, offsets, locations, active, 
N_axial, N_azimuthal, angular_step_axial, angular_step_azimuthal, N_u, N_v, size_u, size_v, 
activity_size_x, activity_size_y, activity_size_z, attenuation_size_x, attenuation_size_y, attenuation_size_z, 
T_activity_x, T_activity_y, T_activity_z, R_activity_x, R_activity_y, R_activity_z, 
T_attenuation_x, T_attenuation_y, T_attenuation_z, R_attenuation_x, R_attenuation_y, R_attenuation_z, 
use_gpu, N_samples, sample_step, background, background_attenuation, truncate_negative_values,direction,block_size): 
    """PET projection; output projection data is compressed. """
    N_locations = locations.shape[0] 
    #accept attenuation=None: 
    if attenuation == None: 
        attenuation = numpy.zeros((0,0,0))
    descriptor = [{'name':'projection',             'type':'array',   'value':None,   'dtype':float32,  'size':(N_locations), }, 
                  {'name':'activity',               'type':'array',   'value':activity}, 
                  {'name':'N_activity_x',           'type':'uint',    'value':activity.shape[0]}, 
                  {'name':'N_activity_y',           'type':'uint',    'value':activity.shape[1]}, 
                  {'name':'N_activity_z',           'type':'uint',    'value':activity.shape[2]}, 
                  {'name':'activity_size_x',        'type':'float',   'value':activity_size_x}, 
                  {'name':'activity_size_y',        'type':'float',   'value':activity_size_y}, 
                  {'name':'activity_size_z',        'type':'float',   'value':activity_size_z}, 
                  
                  {'name':'T_activity_x',           'type':'float',   'value':T_activity_x}, 
                  {'name':'T_activity_y',           'type':'float',   'value':T_activity_y}, 
                  {'name':'T_activity_z',           'type':'float',   'value':T_activity_z}, 
                  {'name':'R_activity_x',           'type':'float',   'value':R_activity_x}, 
                  {'name':'R_activity_y',           'type':'float',   'value':R_activity_y}, 
                  {'name':'R_activity_z',           'type':'float',   'value':R_activity_z}, 

                  {'name':'attenuation',            'type':'array',   'value':attenuation}, 
                  {'name':'N_attenuation_x',        'type':'uint',    'value':attenuation.shape[0]}, 
                  {'name':'N_attenuation_y',        'type':'uint',    'value':attenuation.shape[1]}, 
                  {'name':'N_attenuation_z',        'type':'uint',    'value':attenuation.shape[2]}, 
                  {'name':'attenuation_size_x',     'type':'float',   'value':attenuation_size_x}, 
                  {'name':'attenuation_size_y',     'type':'float',   'value':attenuation_size_y}, 
                  {'name':'attenuation_size_z',     'type':'float',   'value':attenuation_size_z}, 
 
                  {'name':'T_attenuation_x',        'type':'float',   'value':T_attenuation_x}, 
                  {'name':'T_attenuation_y',        'type':'float',   'value':T_attenuation_y}, 
                  {'name':'T_attenuation_z',        'type':'float',   'value':T_attenuation_z}, 
                  {'name':'R_attenuation_x',        'type':'float',   'value':R_attenuation_x}, 
                  {'name':'R_attenuation_y',        'type':'float',   'value':R_attenuation_y}, 
                  {'name':'R_attenuation_z',        'type':'float',   'value':R_attenuation_z}, 

                  {'name':'N_axial',                'type':'uint',    'value':N_axial}, 
                  {'name':'N_azimuthal',            'type':'uint',    'value':N_azimuthal}, 
                  {'name':'angular_step_axial',     'type':'float',   'value':angular_step_axial}, 
                  {'name':'angular_step_azimuthal', 'type':'float',   'value':angular_step_azimuthal},
                  {'name':'N_u',                    'type':'uint',    'value':N_u}, 
                  {'name':'N_v',                    'type':'uint',    'value':N_v}, 
                  {'name':'size_u',                 'type':'float',   'value':size_u}, 
                  {'name':'size_v',                 'type':'float',   'value':size_v}, 

                  {'name':'N_locations',            'type':'uint',    'value':N_locations},
                 
                  {'name':'offsets',                'type':'array',   'value':offsets}, 
                  {'name':'locations',              'type':'array',   'value':locations}, 
                  {'name':'active',                 'type':'array',   'value':active}, 

                  {'name':'N_samples',                'type':'uint',    'value':N_samples}, 
                  {'name':'sample_step',              'type':'float',   'value':sample_step}, 
                  {'name':'background',               'type':'float',   'value':background},
                  {'name':'background_attenuation',   'type':'float',   'value':background_attenuation},  
                  {'name':'truncate_negative_values', 'type':'uint',    'value':truncate_negative_values},  

                  {'name':'use_gpu',                  'type':'uint',    'value':use_gpu}, 
                  {'name':'direction',                'type':'uint',    'value':direction}, 
                  {'name':'block_size',               'type':'uint',    'value':block_size}, 
                  ]
    r = call_c_function( niftyrec_c.PET_project_compressed, descriptor ) 
    if not r.status == status_success(): 
        raise ErrorInCFunction("The execution of 'PET_project_compressed' was unsuccessful.",r.status,'niftyrec_c.PET_project_compressed')
    return r.dictionary["projection"]



def PET_project_compressed_test(activity, attenuation, N_axial, N_azimuthal, offsets, locations, active): 
    N_locations = locations.shape[0]
    #accept attenuation=None: 
    if attenuation == None: 
        attenuation = numpy.zeros((0,0,0))
    descriptor = [{'name':'projection',             'type':'array',   'value':None,   'dtype':float32,  'size':(N_locations),  }, 
                  {'name':'activity',               'type':'array',   'value':activity}, 
                  {'name':'N_activity_x',           'type':'uint',    'value':activity.shape[0]}, 
                  {'name':'N_activity_y',           'type':'uint',    'value':activity.shape[1]}, 
                  {'name':'N_activity_z',           'type':'uint',    'value':activity.shape[2]}, 

                  {'name':'attenuation',            'type':'array',   'value':attenuation}, 
                  {'name':'N_attenuation_x',        'type':'uint',    'value':attenuation.shape[0]}, 
                  {'name':'N_attenuation_y',        'type':'uint',    'value':attenuation.shape[1]}, 
                  {'name':'N_attenuation_z',        'type':'uint',    'value':attenuation.shape[2]}, 

                  {'name':'N_axial',                'type':'uint',    'value':N_axial}, 
                  {'name':'N_azimuthal',            'type':'uint',    'value':N_azimuthal}, 
                  {'name':'N_locations',            'type':'uint',    'value':N_locations},
                 
                  {'name':'offsets',                'type':'array',   'value':offsets}, 
                  {'name':'locations',              'type':'array',   'value':locations}, 
                  {'name':'active',                 'type':'array',   'value':active}, ]
    r = call_c_function( niftyrec_c.PET_project_compressed_test, descriptor ) 
    if not r.status == status_success(): 
        raise ErrorInCFunction("The execution of 'PET_project_compressed_test' was unsuccessful.",r.status,'niftyrec_c.PET_project_compressed_test')
    return r.dictionary["projection"]


                           

def PET_backproject_compressed(projection_data, attenuation, offsets, locations, active, 
N_axial, N_azimuthal, angular_step_axial, angular_step_azimuthal, N_u, N_v, size_u, size_v, 
N_activity_x, N_activity_y, N_activity_z, 
activity_size_x, activity_size_y, activity_size_z, 
attenuation_size_x, attenuation_size_y, attenuation_size_z, 
T_activity_x, T_activity_y, T_activity_z, R_activity_x, R_activity_y, R_activity_z, 
T_attenuation_x, T_attenuation_y, T_attenuation_z, R_attenuation_x, R_attenuation_y, R_attenuation_z, 
use_gpu, N_samples, sample_step, background, background_attenuation, direction, block_size): 
    """PET back-projection; input projection data is compressed. """
    N_locations = locations.shape[0] 
    #accept attenuation=None: 
    if attenuation == None: 
        attenuation = numpy.zeros((0,0,0))
    descriptor = [{'name':'back_projection',        'type':'array',   'value':None,   'dtype':float32,  'size':(N_activity_x,N_activity_y,N_activity_z),  }, # 'swapaxes':(0,2)  }, 
                  {'name':'N_activity_x',           'type':'uint',    'value':N_activity_x}, 
                  {'name':'N_activity_y',           'type':'uint',    'value':N_activity_y}, 
                  {'name':'N_activity_z',           'type':'uint',    'value':N_activity_z}, 
                  {'name':'activity_size_x',        'type':'float',   'value':activity_size_x}, 
                  {'name':'activity_size_y',        'type':'float',   'value':activity_size_y}, 
                  {'name':'activity_size_z',        'type':'float',   'value':activity_size_z}, 
                  
                  {'name':'T_activity_x',           'type':'float',   'value':T_activity_x}, 
                  {'name':'T_activity_y',           'type':'float',   'value':T_activity_y}, 
                  {'name':'T_activity_z',           'type':'float',   'value':T_activity_z}, 
                  {'name':'R_activity_x',           'type':'float',   'value':R_activity_x}, 
                  {'name':'R_activity_y',           'type':'float',   'value':R_activity_y}, 
                  {'name':'R_activity_z',           'type':'float',   'value':R_activity_z}, 

                  {'name':'attenuation',            'type':'array',   'value':attenuation}, 
                  {'name':'N_attenuation_x',        'type':'uint',    'value':attenuation.shape[0]}, 
                  {'name':'N_attenuation_y',        'type':'uint',    'value':attenuation.shape[1]}, 
                  {'name':'N_attenuation_z',        'type':'uint',    'value':attenuation.shape[2]}, 
                  {'name':'attenuation_size_x',     'type':'float',   'value':attenuation_size_x}, 
                  {'name':'attenuation_size_y',     'type':'float',   'value':attenuation_size_y}, 
                  {'name':'attenuation_size_z',     'type':'float',   'value':attenuation_size_z}, 

                  {'name':'T_attenuation_x',        'type':'float',   'value':T_attenuation_x}, 
                  {'name':'T_attenuation_y',        'type':'float',   'value':T_attenuation_y}, 
                  {'name':'T_attenuation_z',        'type':'float',   'value':T_attenuation_z}, 
                  {'name':'R_attenuation_x',        'type':'float',   'value':R_attenuation_x}, 
                  {'name':'R_attenuation_y',        'type':'float',   'value':R_attenuation_y}, 
                  {'name':'R_attenuation_z',        'type':'float',   'value':R_attenuation_z}, 

                  {'name':'N_axial',                'type':'uint',    'value':N_axial}, 
                  {'name':'N_azimuthal',            'type':'uint',    'value':N_azimuthal}, 
                  {'name':'angular_step_axial',     'type':'float',   'value':angular_step_axial}, 
                  {'name':'angular_step_azimuthal', 'type':'float',   'value':angular_step_azimuthal},
                  {'name':'N_u',                    'type':'uint',    'value':N_u}, 
                  {'name':'N_v',                    'type':'uint',    'value':N_v}, 
                  {'name':'size_u',                 'type':'float',   'value':size_u}, 
                  {'name':'size_v',                 'type':'float',   'value':size_v}, 

                  {'name':'N_locations',            'type':'uint',    'value':N_locations},
                 
                  {'name':'offsets',                'type':'array',   'value':offsets}, 
                  {'name':'locations',              'type':'array',   'value':locations}, 
                  {'name':'active',                 'type':'array',   'value':active}, 
                  {'name':'projection_data',        'type':'array',   'value':projection_data}, 
           
                  {'name':'use_gpu',                'type':'uint',    'value':use_gpu}, 
                  {'name':'N_samples',              'type':'uint',    'value':N_samples}, 
                  {'name':'sample_step',            'type':'float',   'value':sample_step}, 
                  {'name':'background_activity',    'type':'float',   'value':background}, 
                  {'name':'background_attenuation', 'type':'float',   'value':background_attenuation}, 
                  {'name':'direction',              'type':'uint',    'value':direction},
                  {'name':'block_size',             'type':'uint',    'value':block_size},  ]
    r = call_c_function( niftyrec_c.PET_backproject_compressed, descriptor ) 
    if not r.status == status_success(): 
        raise ErrorInCFunction("The execution of 'PET_backproject_compressed' was unsuccessful.",r.status,'niftyrec_c.PET_backproject_compressed')
    return r.dictionary['back_projection']




def ET_spherical_phantom(voxels,size,center,radius,inner_value,outer_value): 
    """PET back-projection; input projection data is compressed. """
    descriptor = [{'name':'image',                 'type':'array', 'value':None,   'dtype':float32,  'size':(voxels[0],voxels[1],voxels[2]),  },#  'swapaxes':(0,2)  }, 
                  {'name':'Nx',                    'type':'uint',  'value':voxels[0]}, 
                  {'name':'Ny',                    'type':'uint',  'value':voxels[1]}, 
                  {'name':'Nz',                    'type':'uint',  'value':voxels[2]}, 
                  {'name':'sizex',                 'type':'float', 'value':size[0]},
                  {'name':'sizey',                 'type':'float', 'value':size[1]},
                  {'name':'sizez',                 'type':'float', 'value':size[2]},
                  {'name':'centerx',               'type':'float', 'value':center[0]},
                  {'name':'centery',               'type':'float', 'value':center[1]},
                  {'name':'centerz',               'type':'float', 'value':center[2]},
                  {'name':'radius',                'type':'float', 'value':radius},
                  {'name':'inner_value',           'type':'float', 'value':inner_value},
                  {'name':'outer_value',           'type':'float', 'value':outer_value},  ] 
    r = call_c_function( niftyrec_c.ET_spherical_phantom, descriptor ) 
    if not r.status == status_success(): 
        raise ErrorInCFunction("The execution of 'ET_spherical_phantom' was unsuccessful.",r.status,'niftyrec_c.ET_spherical_phantom')
    return r.dictionary['image']



def ET_cylindrical_phantom(voxels,size,center,radius,length,axis,inner_value,outer_value): 
    """PET back-projection; input projection data is compressed. """
    descriptor = [{'name':'image',                 'type':'array', 'value':None,   'dtype':float32,  'size':(voxels[0],voxels[1],voxels[2]),  },#  'swapaxes':(0,2)  }, 
                  {'name':'Nx',                    'type':'uint',  'value':voxels[0]}, 
                  {'name':'Ny',                    'type':'uint',  'value':voxels[1]}, 
                  {'name':'Nz',                    'type':'uint',  'value':voxels[2]}, 
                  {'name':'sizex',                 'type':'float', 'value':size[0]},
                  {'name':'sizey',                 'type':'float', 'value':size[1]},
                  {'name':'sizez',                 'type':'float', 'value':size[2]},
                  {'name':'centerx',               'type':'float', 'value':center[0]},
                  {'name':'centery',               'type':'float', 'value':center[1]},
                  {'name':'centerz',               'type':'float', 'value':center[2]},
                  {'name':'radius',                'type':'float', 'value':radius},
                  {'name':'length',                'type':'float', 'value':length},
                  {'name':'axis',                  'type':'uint',  'value':axis},
                  {'name':'inner_value',           'type':'float', 'value':inner_value},
                  {'name':'outer_value',           'type':'float', 'value':outer_value},  ] 
    r = call_c_function( niftyrec_c.ET_cylindrical_phantom, descriptor ) 
    if not r.status == status_success(): 
        raise ErrorInCFunction("The execution of 'ET_cylindrical_phantom' was unsuccessful.",r.status,'niftyrec_c.ET_cylindrical_phantom')
    return r.dictionary['image']



def ET_spheres_ring_phantom(voxels,size,center,ring_radius,min_sphere_radius,max_sphere_radius,N_spheres=6,inner_value=1.0,outer_value=0.0,taper=0,axis=0): 
    """PET back-projection; input projection data is compressed. """
    descriptor = [{'name':'image',                 'type':'array', 'value':None,   'dtype':float32,  'size':(voxels[0],voxels[1],voxels[2]),  }, # 'swapaxes':(0,2)  }, 
                  {'name':'Nx',                    'type':'uint',  'value':voxels[0]}, 
                  {'name':'Ny',                    'type':'uint',  'value':voxels[1]}, 
                  {'name':'Nz',                    'type':'uint',  'value':voxels[2]}, 
                  {'name':'sizex',                 'type':'float', 'value':size[0]},
                  {'name':'sizey',                 'type':'float', 'value':size[1]},
                  {'name':'sizez',                 'type':'float', 'value':size[2]},
                  {'name':'centerx',               'type':'float', 'value':center[0]},
                  {'name':'centery',               'type':'float', 'value':center[1]},
                  {'name':'centerz',               'type':'float', 'value':center[2]},
                  {'name':'ring_radius',           'type':'float', 'value':ring_radius}, 
                  {'name':'min_sphere_radius',     'type':'float', 'value':min_sphere_radius}, 
                  {'name':'max_sphere_radius',     'type':'float', 'value':max_sphere_radius}, 
                  {'name':'N_spheres',             'type':'uint',  'value':N_spheres}, 
                  {'name':'inner_value',           'type':'float', 'value':inner_value},
                  {'name':'outer_value',           'type':'float', 'value':outer_value},  
                  {'name':'taper',                 'type':'float', 'value':taper},  
                  {'name':'ring_axis',             'type':'uint',  'value':axis}, ] 
    r = call_c_function( niftyrec_c.ET_spheres_ring_phantom, descriptor ) 
    if not r.status == status_success(): 
        raise ErrorInCFunction("The execution of 'ET_spheres_ring_phantom' was unsuccessful.",r.status,'niftyrec_c.ET_spheres_ring_phantom')
    return r.dictionary['image']


    
    
    

def SPECT_project_parallelholes(activity,attenuation,camera_trajectory,PSF,use_gpu=0): 
    """SPECT projection; parallel-holes geometry. """
    descriptor = [    ] 
    r = call_c_function( niftyrec_c.SPECT_project_parallelholes, descriptor ) 
    if not r.status == status_success(): 
        raise ErrorInCFunction("The execution of 'SPECT_project_parallelholes' was unsuccessful.",r.status,'niftyrec_c.SPECT_project_parallelholes')
    return r.dictionary


def SPECT_backproject_parallelholes(projection_data,attenuation,camera_trajectory,PSF,use_gpu=0): 
    """SPECT back-projection; parallel-holes geometry. """
    descriptor = [    ] 
    r = call_c_function( niftyrec_c.SPECT_backproject_parallelholes, descriptor ) 
    if not r.status == status_success(): 
        raise ErrorInCFunction("The execution of 'SPECT_backproject_parallelholes' was unsuccessful.",r.status,'niftyrec_c.SPECT_backproject_parallelholes')
    return r.dictionary 


def CT_project_conebeam(attenuation,camera_trajectory,source_trajectory,use_gpu=0): 
    """Transmission imaging projection; cone-beam geometry. """
    descriptor = [    ] 
    r = call_c_function( niftyrec_c.CT_project_conebeam, descriptor ) 
    if not r.status == status_success(): 
        raise ErrorInCFunction("The execution of 'CT_project_conebeam' was unsuccessful.",r.status,'niftyrec_c.CT_project_conebeam')
    return r.dictionary     


def CT_backproject_conebeam(projection_data,camera_trajectory,source_trajectory,use_gpu=0): 
    """Transmission imaging back-projection; cone-beam geometry. """
    descriptor = [    ] 
    r = call_c_function( niftyrec_c.CT_backproject_conebeam, descriptor ) 
    if not r.status == status_success(): 
        raise ErrorInCFunction("The execution of 'CT_backproject_conebeam' was unsuccessful.",r.status,'niftyrec_c.CT_backproject_conebeam')
    return r.dictionary             


def CT_project_parallelbeam(attenuation,camera_trajectory,source_trajectory,use_gpu=0): 
    """Transmission imaging projection; parallel-beam geometry. """
    descriptor = [    ] 
    r = call_c_function( niftyrec_c.CT_project_parallelbeam, descriptor ) 
    if not r.status == status_success(): 
        raise ErrorInCFunction("The execution of 'CT_project_parallelbeam' was unsuccessful.",r.status,'niftyrec_c.CT_project_parallelbeam')
    return r.dictionary         


def CT_backproject_parallelbeam(attenuation,camera_trajectory,source_trajectory,use_gpu=0): 
    """Transmission imaging back-projection; parallel-beam geometry. """
    descriptor = [    ] 
    r = call_c_function( niftyrec_c.CT_backproject_parallelbeam, descriptor ) 
    if not r.status == status_success(): 
        raise ErrorInCFunction("The execution of 'CT_backproject_parallelbeam' was unsuccessful.",r.status,'niftyrec_c.CT_backproject_parallelbeam')
    return r.dictionary         


