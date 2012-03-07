#!/usr/bin/ipython 

import matplotlib
matplotlib.use('GTKAgg') # do this before importing pylab
from MozaikLite.framework.experiment import MeasureOrientationTuningFullfield, MeasureSpontaneousActivity, MeasureNaturalImagesWithEyeMovement
import config
from pyNN import nest as sim
from MozaikLite.models.model import JensModel
from MozaikLite.framework.experiment_controller import run_experiments, setup_experiments
from MozaikLite.visualization.plotting import GSynPlot,RasterPlot,VmPlot,CyclicTuningCurvePlot,OverviewPlot, ConductanceSignalListPlot, RetinalInputMovie, ActivityMovie
from MozaikLite.analysis.analysis import AveragedOrientationTuning,  GSTA, Precision
from MozaikLite.visualization.jens_paper_plots import Figure2
from MozaikLite.storage.datastore import Hdf5DataStore,PickledDataStore
from NeuroTools.parameters import ParameterSet
from MozaikLite.storage.queries import TagBasedQuery, select_result_sheet_query




if True:
    params = setup_experiments('FFI',sim)
    jens_model = JensModel(sim,params)
    
    experiment_list =   [
                           #MeasureSpontaneousActivity(jens_model,duration=147*7),
                           #MeasureOrientationTuningFullfield(jens_model,num_orientations=8,spatial_frequency=0.8,temporal_frequency=2,grating_duration=148*7,num_trials=10),
                           MeasureOrientationTuningFullfield(jens_model,num_orientations=8,spatial_frequency=0.8,temporal_frequency=2,grating_duration=57*7,num_trials=2),
                           #MeasureOrientationTuningFullfield(jens_model,num_orientations=8,spatial_frequency=0.8,temporal_frequency=2,grating_duration=148*7,num_trials=3),
                        ]

    data_store = run_experiments(jens_model,experiment_list)
else:
    data_store = PickledDataStore(load=True,parameters=ParameterSet({'root_directory':'medium_B'}))

print config.hp.heap()

0/0


AveragedOrientationTuning(data_store,ParameterSet({})).analyse()
GSTA(data_store,ParameterSet({'neurons' : [0], 'length' : 250.0 }),tags=['GSTA1']).analyse()
Precision(select_result_sheet_query(data_store,"V1_Exc"),ParameterSet({'neurons' : [0], 'bin_length' : 10.0 })).analyse()

OverviewPlot(data_store,ParameterSet({'sheet_name' : 'V1_Exc', 'neuron' : 0, 'sheet_activity' : {'scatter': True,'frame_rate': 3, 'bin_width' : 50.0, 'sheet_name' : 'X_ON', 'resolution' : 40}})).plot()
OverviewPlot(data_store,ParameterSet({'sheet_name' : 'V1_Inh', 'neuron' : 0, 'sheet_activity' : {}})).plot()
OverviewPlot(data_store,ParameterSet({'sheet_name' : 'X_ON', 'neuron' : 0, 'sheet_activity' : {}})).plot()
OverviewPlot(data_store,ParameterSet({'sheet_name' : 'X_OFF', 'neuron' : 0, 'sheet_activity' : {}})).plot()
Figure2(data_store,ParameterSet({'sheet_name' : 'V1_Exc'})).plot()
#RetinalInputMovie(data_store,ParameterSet({'frame_rate': 10})).plot()


import pylab
pylab.show()
