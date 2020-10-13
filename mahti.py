# adapted from the Neale platform module
# levi.keller@aalto.fi
'''Set up Environment Modules on CSC mahti
   Numpy installed in userspace with pip3'''

#  Copyright (C) 2017 The authors of Py-ChemShell
#
#  This file is part of Py-ChemShell.
#
#  Py-ChemShell is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  Py-ChemShell is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with Py-ChemShell.  If not, see
#  <http://www.gnu.org/licenses/>.

def init(args, utils=None, load=[], unload=[]):
    '''
    "utils" is not passed - not sure how this is supposed to work, load the necessary modules manually
    '''
    print("autoloading of modules disabled - issue 'module load cmake netlib-scalapack'")

#    from os             import environ, path, sep
#    from re             import sub
#    from importlib.util import spec_from_file_location, module_from_spec

#    intel_version  = '2016.1.10'
#    python_version = '3.6.8'

#    toloads = { 'intel_cs' :'intel'
#              }

    # MODULESHOME on the platform--this is basically the only variable you need to edit when create this file for a new platform
#    print("\n >>> Setting up Environment Modules on CSC Mahti for building ChemShell...\n")
#    module = utils.getEnvModules(path.join(sep, 'appl', 'spack', 'v014', 'install-tree', 'gcc-4.8.5','lmod-8.3-kag3x6','lmod','lmod'))

#    environ.setdefault('LOADEDMODULES', '')

    # modules to load
    # load = utils.getModulesToLoad(toloads, load)

    # conflicting modules to unload
#    unload += [ ]

    # unload conflicting modules
#    module.module('unload', *unload)

    # load necessary modules
#    module.module('load', *load)

    # print a summary
#    module.module('list')

#./setup --mpi --mpiexec srun  --fc mpif90 --cc mpicc --gulp $PWD/chemsh/interfaces/gulp/gulp-5.2  --gulp-version 5.2 --fhiaims /scratch/project_2001157/levi/FHIaims/lib/libaims.200828.scalapack.mpi.so --scalapack --scalapack_flags " -L${MKLROOT}/lib/intel64_lin -I${MKLROOT}/include -lmkl_scalapack_lp64 -lmkl_intel_lp64 -lmkl_sequential -lmkl_core -lmkl_blacs_openmpi_lp64 -lpthread -ldl"


#    args.mpi       =  True
#    args.fc        = 'mpif90'
#    args.cc        = 'mpicc'
#    args.mpiexec   = 'srun'
#    args.mkl       = '/cm/shared/hartree/intel/intel_cs/%s/mkl'%intel_version
#    args.mkl       = path.join(sep, 'cm', 'shared', 'hartree', 'intel', 'intel_cs', intel_version, 'mkl', 'lib', 'intel64')
#    args.scalapack_flags = ' -lmkl_scalapack_lp64 -lmkl_intel_lp64 -lmkl_sequential -lmkl_core -lmkl_blacs_openmpi_lp64 -lpthread -ldl'
#    args.scalapack = '/appl/opt/cluster_studio_xe2020/compilers_and_libraries_2020.1.217/linux/mkl'
#    args.pythonlib = path.join(sep, 'cm', 'shared', 'hartree', 'python3', python_version, 'lib',     'libpython3.6m.so')
#    args.pythondir = path.join(sep, 'cm', 'shared', 'hartree', 'python3', python_version, 'include', 'python3.6m')
#    args.ld_path   = [ path.join(sep, 'cm', 'shared', 'hartree', 'intel', 'intel_cs', intel_version, 'lib', 'intel64') ]

def setup(args):
    ''''''

    from os import path, sep

    # force to build parallel binary on SCARF
    args.mpi       =  True
    args.i8        =  False
    args.fc        = 'mpif90'
    args.fflags.append(' -march=native -ffree-line-length-none -g')
    args.cc        = 'mpicc'
    args.cflags.append(' -march=native -DNDEBUG -funroll-loops')
    args.mpiexec   = 'srun'
    args.blas = args.lapack = path.join(sep, 'appl','spack','v014','install-tree','gcc-9.3.0','openblas-0.3.10-ox6ff3','lib')
    args.scalapack = path.join(sep, 'appl','spack','v014','install-tree','gcc-9.3.0','netlib-scalapack-2.1.0-xeslcn','lib')
    args.scalapack_flags = "-lopenblas -lscalapack"

    # /apps/python/3.6.5/intel/17.0.2/include/python3.6m/
#    args.pythonlib = path.join(sep, 'apps', 'python', python_subversion, 'intel', intel_version, 'lib', 'libpython%sm.so'%python_version)
#    args.pythondir = path.join(sep, 'apps', 'python', python_subversion, 'intel', intel_version, 'include', 'python%sm'%python_version)

#    mkl_suffix = '_lp64'
#    args.mkl_flags       = '-lmkl_core -lmkl_intel%s -lpthread -ldl -lmkl_sequential'%mkl_suffix
#    args.scalapack_flags = '-lmkl_blacs_openmpi%s -lmkl_scalapack%s'%(mkl_suffix, mkl_suffix)

    platfmodule = args.__import('platforms', path.join(args.__CHEMSH_ROOT, 'chemsh', 'utils', 'platforms', '__init__.py'))

    # make `chemsh` a bash/python "heredoc" for the users' convenience
    # args.__bash_header = [ '#!/bin/bash --login', 'module load {}'.format(python_module), 'read -r -d \\\"\\\" CMD << EOF' ]
    # args.__bash_footer = platfmodule.__bash_footer


def run(args):
    '''Submit the job'''

    from math       import ceil
    from os         import environ, path
    from subprocess import check_output

#    initPlatform(load=args.load_modules, unload=args.unload_modules)

    environ['CHEMSH_EXEC']        = args.__CHEMSH_EXEC
    environ['CHEMSH_NPROCS']      = str(args.nprocs)
    environ['CHEMSH_NWORKGROUPS'] = str(args.nworkgroups)
    environ['CHEMSH_INPUT']       = args.filenames
    environ['CHEMSH_OUTPUT']      = args.jobname+'.log'
    environ['CHEMSH_WRAPPER']     = args.wrapper

    nnodes = ceil(args.nprocs/128)
#    ncpus_per_node = ceil(args.nprocs/args.nnodes)
    if not args.nodename:
        args.nodename = 'defq'

# YL TODO: -o and -e
    job_id = check_output([ 'sbatch',
                            '--get-user-env',
                            '--ntasks-per-node', str(128),
                            '-A',     args.account,
                            '-J',     args.jobname,
                            '-o',     args.jobname+'.log',
                            '-e',     args.jobname+'.err',
                            '-t',     args.walltime,
                            '-p',     args.nodename,
                            '-n', str(args.nprocs),
                            path.join(path.dirname(path.realpath(__file__)), 'mahti.sh')
                            ])

    print("\n\n >>>", job_id.decode().rstrip(), "submitted to mahti compute nodes\n\n")




