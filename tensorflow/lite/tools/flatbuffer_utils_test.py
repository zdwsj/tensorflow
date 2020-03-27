# Copyright 2020 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Tests for flatbuffer_utils.py."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from tensorflow.lite.tools import flatbuffer_utils
from tensorflow.lite.tools import test_utils
from tensorflow.python.framework import test_util
from tensorflow.python.platform import test


class WriteReadModelTest(test_util.TensorFlowTestCase):

  def testWriteReadModel(self):
    # 1. SETUP
    # Define the initial model
    initial_model = test_utils.build_mock_model_python_object()
    # Define temporary files
    tmp_dir = self.get_temp_dir()
    model_filename = os.path.join(tmp_dir, 'model.tflite')

    # 2. INVOKE
    # Invoke the write_model and read_model functions
    flatbuffer_utils.write_model(initial_model, model_filename)
    final_model = flatbuffer_utils.read_model(model_filename)

    # 3. VALIDATE
    # Validate that the initial and final models are the same
    # Validate the description
    self.assertEqual(initial_model.description, final_model.description)
    # Validate the main subgraph's name, inputs, outputs, operators and tensors
    initial_subgraph = initial_model.subgraphs[0]
    final_subgraph = final_model.subgraphs[0]
    self.assertEqual(initial_subgraph.name, final_subgraph.name)
    for i in range(len(initial_subgraph.inputs)):
      self.assertEqual(initial_subgraph.inputs[i], final_subgraph.inputs[i])
    for i in range(len(initial_subgraph.outputs)):
      self.assertEqual(initial_subgraph.outputs[i], final_subgraph.outputs[i])
    for i in range(len(initial_subgraph.operators)):
      self.assertEqual(initial_subgraph.operators[i].opcodeIndex,
                       final_subgraph.operators[i].opcodeIndex)
    initial_tensors = initial_subgraph.tensors
    final_tensors = final_subgraph.tensors
    for i in range(len(initial_tensors)):
      self.assertEqual(initial_tensors[i].name, final_tensors[i].name)
      self.assertEqual(initial_tensors[i].type, final_tensors[i].type)
      self.assertEqual(initial_tensors[i].buffer, final_tensors[i].buffer)
      for j in range(len(initial_tensors[i].shape)):
        self.assertEqual(initial_tensors[i].shape[j], final_tensors[i].shape[j])
    # Validate the first valid buffer (index 0 is always None)
    initial_buffer = initial_model.buffers[1].data
    final_buffer = final_model.buffers[1].data
    for i in range(initial_buffer.size):
      self.assertEqual(initial_buffer.data[i], final_buffer.data[i])


class StripStringsTest(test_util.TensorFlowTestCase):

  def testStripStrings(self):
    # 1. SETUP
    # Define the initial model
    initial_model = test_utils.build_mock_model_python_object()

    # 2. INVOKE
    # Invoke the strip_strings function
    final_model = flatbuffer_utils.strip_strings(initial_model)

    # 3. VALIDATE
    # Validate that the initial and final models are the same except strings
    # Validate the description
    self.assertNotEqual('', initial_model.description)
    self.assertEqual('', final_model.description)
    # Validate the main subgraph's name, inputs, outputs, operators and tensors
    initial_subgraph = initial_model.subgraphs[0]
    final_subgraph = final_model.subgraphs[0]
    self.assertNotEqual('', initial_model.subgraphs[0].name)
    self.assertEqual('', final_model.subgraphs[0].name)
    for i in range(len(initial_subgraph.inputs)):
      self.assertEqual(initial_subgraph.inputs[i], final_subgraph.inputs[i])
    for i in range(len(initial_subgraph.outputs)):
      self.assertEqual(initial_subgraph.outputs[i], final_subgraph.outputs[i])
    for i in range(len(initial_subgraph.operators)):
      self.assertEqual(initial_subgraph.operators[i].opcodeIndex,
                       final_subgraph.operators[i].opcodeIndex)
    initial_tensors = initial_subgraph.tensors
    final_tensors = final_subgraph.tensors
    for i in range(len(initial_tensors)):
      self.assertNotEqual('', initial_tensors[i].name)
      self.assertEqual('', final_tensors[i].name)
      self.assertEqual(initial_tensors[i].type, final_tensors[i].type)
      self.assertEqual(initial_tensors[i].buffer, final_tensors[i].buffer)
      for j in range(len(initial_tensors[i].shape)):
        self.assertEqual(initial_tensors[i].shape[j], final_tensors[i].shape[j])
    # Validate the first valid buffer (index 0 is always None)
    initial_buffer = initial_model.buffers[1].data
    final_buffer = final_model.buffers[1].data
    for i in range(initial_buffer.size):
      self.assertEqual(initial_buffer.data[i], final_buffer.data[i])


class RandomizeWeightsTest(test_util.TensorFlowTestCase):

  def testRandomizeWeights(self):
    # 1. SETUP
    # Define the initial model
    initial_model = test_utils.build_mock_model_python_object()

    # 2. INVOKE
    # Invoke the randomize_weights function
    final_model = flatbuffer_utils.randomize_weights(initial_model)

    # 3. VALIDATE
    # Validate that the initial and final models are the same, except that
    # the weights in the model buffer have been modified (i.e, randomized)
    # Validate the description
    self.assertEqual(initial_model.description, final_model.description)
    # Validate the main subgraph's name, inputs, outputs, operators and tensors
    initial_subgraph = initial_model.subgraphs[0]
    final_subgraph = final_model.subgraphs[0]
    self.assertEqual(initial_subgraph.name, final_subgraph.name)
    for i in range(len(initial_subgraph.inputs)):
      self.assertEqual(initial_subgraph.inputs[i], final_subgraph.inputs[i])
    for i in range(len(initial_subgraph.outputs)):
      self.assertEqual(initial_subgraph.outputs[i], final_subgraph.outputs[i])
    for i in range(len(initial_subgraph.operators)):
      self.assertEqual(initial_subgraph.operators[i].opcodeIndex,
                       final_subgraph.operators[i].opcodeIndex)
    initial_tensors = initial_subgraph.tensors
    final_tensors = final_subgraph.tensors
    for i in range(len(initial_tensors)):
      self.assertEqual(initial_tensors[i].name, final_tensors[i].name)
      self.assertEqual(initial_tensors[i].type, final_tensors[i].type)
      self.assertEqual(initial_tensors[i].buffer, final_tensors[i].buffer)
      for j in range(len(initial_tensors[i].shape)):
        self.assertEqual(initial_tensors[i].shape[j], final_tensors[i].shape[j])
    # Validate the first valid buffer (index 0 is always None)
    initial_buffer = initial_model.buffers[1].data
    final_buffer = final_model.buffers[1].data
    for j in range(initial_buffer.size):
      self.assertNotEqual(initial_buffer.data[j], final_buffer.data[j])


if __name__ == '__main__':
  test.main()