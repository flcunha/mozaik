"""
This module contains the definition of the AnalysisDataStructure API and implementation of 
some basic analysis data structures.
"""

import numpy
from MozaikLite.stimuli.stimulus_generator import parse_stimuls_id

class AnalysisDataStructure(object):
      """
      AnalysisDataStructure encupsulates data that a certain Analysis class generates.
      An analysis class can generate several AnalysisDataStructure's and one AnalysisDataStructure
      can be generated by several Analysis classes
      the goal is to offer a common interface of such data for plotting 
      i.e. many analysis can generate 2D tuning curves of several kinds but they all
      share common data structure and can be plotted in a common way
      
      identifier - 
          An important parameter of each AnalysisDataStructure is identifier which is used to 
          identify data structures of common type in storage facilities.
          Currently different datastructures with common interface should share the identifiers
          but it is not clear this is needed. If it turns out such sharing is not neccessary it 
          might be abolished and there will be one-to-one mapping between AnalysisDataStructure classes
          and identifiers.
      
      tags - 
          Often it might be difficult to design a filter to extract the right set of recordings or analysis 
          data structures for a given analysis or visualization. For example it might be possible that many 
          types of analysis will produce the same AnalysisDataStructure but you want to plot only those
          produced from one specific one in a single figure. It might be difficult or impossible to write 
          a filter that picks only the right one. On the other hand we do not want users to define multiple 
          AnalysisDataStructures that hold the same kind of data only to be able to tell them appart.
                  
          Therefore, we also allow all analysis data structures to contain a list of tags
          (which are strings) that one can add during their creation (or later) and use 
          them to later for their identification in DataStore.
          
          However, in general, we encourage users to use filter methods rather that tags to perform their
          plotting/analysis whenever possible!!!!
      """
      identifier = None
      tags = []
      
      def __init__(self,tags=[]):
          self.tags = tags      

          
class TuningCurve(AnalysisDataStructure):
        """
             Tuning curve holds data of a tuning curves with respect to a certain paramter of a stimulus.
             
             It is assumed that all other paramters are either: 
              * collpased (i.e. they have been averaged out such as phase or trials in case of orientation tuning)
              * those that are unclopased should be tread as the paramters of 
                the tuning curve (i.e. orientation tuning curves taken at different contrasts)
            
             sheet_name 
                    - in which sheet the data were recorded
             values     
                    - is a list of lists, members of the outer list correspond 
                      to the value of the tuning curve for a stimulus at the same position in the stimuli_ids
                      the inner lists contain the actual values for the measured neurons
             stimuli_ids 
                    - see values description
             parameter_index 
                    - the parameter position in the stimulus id against which the tuning curve was computed
        """
        
        identifier = 'TuningCurve'
        
        def __init__(self,values,stimuli_ids,parameter_index,sheet_name,tags=[]):
            AnalysisDataStructure.__init__(self,tags)
            self.sheet_name = sheet_name    
            self.values = values
            self.stimuli_ids = stimuli_ids
            self.parameter_index = parameter_index

        def to_dictonary_of_tc_parametrization(self):
            # creat dictionary where stimulus_id indexes all the different 
            # values and corresponding data for the given 
            # neurons throught the range of the paramter against which the tuning curve was computed
            # this groups the data according to the the individual tuning curves to be plotted, each
            # corresponding to different parametrization (ie. contrast for orientation tuning)

            self.d = {}
            for (v,s) in zip(self.values,self.stimuli_ids):
                s = parse_stimuls_id(s)
                val = s.parameters[self.parameter_index]
                s.parameters[self.parameter_index]='x'
                
                if self.d.has_key(str(s)):
                   (a,b) = self.d[str(s)] 
                   a.append(v)
                   b.append(val)
                else:
                   self.d[str(s)]  = ([v],[val]) 
            
            for k in self.d:
                (a,b) = self.d[k]
                self.d[k] = (numpy.array(a),b)
            
            return self.d

class CyclicTuningCurve(TuningCurve):
        """
        TuningCurve with over periodic quantity
        
        perdiod - the period of the parameter over which the tuning curve is measured, i.e. pi for orientation
                  all the values have to be in the range <0,period)
        
        """
        identifier = 'TuningCurve'
        
        def __init__(self,period,*args,**kwargs):
            TuningCurve.__init__(self,*args,**kwargs)
            self.period = period    
            
            # just double check that none of the stimuly has the corresponding parameter larger than period 
            for s in self.stimuli_ids:
                s = parse_stimuls_id(s)
                v = float(s.parameters[self.parameter_index])
                if v < 0 or v >= self.period:
                   raise ValueError("CyclicTuningCurve with period " + str(self.period) + ": "  + str(v) + " does not belong to <0," + str(self.period) + ") range!") 
                
            
            
            

class AnalogSignalList(AnalysisDataStructure):
       """
         This is a simple list of Neo AnalogSignal objects.

         sheet_name - 
                in which sheet the data were recorded
         asl - 
                the variable containing the list of AnalogSignal objects, in the order corresponding to the 
                order of neurons indexes in the indexes parameter
         indexes - 
                list of indexes of neurons in the original Mozaik sheet to which the AnalogSignals correspond
       """
       identifier = 'AnalogSignalList'
        
       def __init__(self,asl,sheet_name,indexes,tags=[]):
           AnalysisDataStructure.__init__(self,tags)
           self.sheet_name = sheet_name    
           self.asl = asl
           self.indexes = indexes

class ConductanceSignalList(AnalysisDataStructure):
       """
         This is a simple list of Neurotools AnalogSignal objects representing the conductances
         The object holds two lists, one for excitatory and one for inhibitory conductances

         sheet_name - 
            in which sheet the data were recorded
         e_asl - 
            the variable containing the list of AnalogSignal objects corresponding to excitatory conductances,
            in the order corresponding to the order of neurons indexes in the indexes parameter
         i_asl - 
            the variable containing the list of AnalogSignal objects corresponding to inhibitory conductances,
            in the order corresponding to the order of neurons indexes in the indexes parameter
         indexes - 
            list of indexes of neurons in the original Mozaik sheet to which the AnalogSignals correspond
       """
       identifier = 'ConductanceSignalList'
        
       def __init__(self,e_con,i_con,sheet_name,indexes,tags=[]):
           AnalysisDataStructure.__init__(self,tags)
           self.sheet_name = sheet_name    
           self.e_con = e_con
           self.i_con = i_con
           self.indexes = indexes

      

class NeurotoolsData(AnalysisDataStructure):
      """
      Turn the recordings into Neurotools data structures that can than be visualized 
      via numerous Neurotools analysis tools
      """
      
      identifier = 'NeurotoolsData'
      
      def __init__(self,spike_data_dict,vm_data_dict,g_syn_e_data_dict,g_syn_i_data_dict,tags=[]):
          AnalysisDataStructure.__init__(self,tags)
          self.vm_data_dict = vm_data_dict
          self.g_syn_e_data_dict = g_syn_e_data_dict
          self.g_syn_i_data_dict = g_syn_i_data_dict
          self.spike_data_dict = spike_data_dict
