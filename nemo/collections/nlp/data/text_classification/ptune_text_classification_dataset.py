# Copyright 2018 The Google AI Language Team Authors and
# The HuggingFace Inc. team.
# Copyright (c) 2020, NVIDIA CORPORATION.  All rights reserved.
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

import json
import os
from typing import Dict, List, Optional

from nemo.core.classes import Dataset
from nemo.core.neural_types import NeuralType, StringLabel, StringType

__all__ = ['PTuneTextClassificationDataset', 'token_wrapper']


def load_file(filename):
    data = []
    with open(filename, "r") as f:
        for line in f.readlines():
            data.append(json.loads(line))
    return data


def token_wrapper(token: str) -> str:
    return 'Ġ' + token


class PTuneTextClassificationDataset(Dataset):
    @property
    def output_types(self) -> Optional[Dict[str, NeuralType]]:
        return {"sentences": [NeuralType(('T'), StringType())], "labels": [NeuralType(('T'), StringLabel())]}

    def __init__(self, input_file: str, sentiments: List[str], data: List[str] = None, prompt: str = 'Sentiment'):
        super().__init__()
        if input_file and not os.path.exists(input_file):
            raise FileNotFoundError(
                f'Data file `{input_file}` not found! Each line of the data file should contain json object'
                f'where `sentence` key maps to sentence and `label` key maps to label'
            )
        if data is None:
            json_data = load_file(input_file)
        else:
            json_data = []
            for line in data:
                json_data.append({'sentence': line + f' {prompt} ', 'label': ''})
        self.x_hs, self.x_ts = [], []
        self.data = json_data

        for d in json_data:
            if d['label'] not in sentiments:
                continue
            self.x_ts.append(d['label'])
            self.x_hs.append(d['sentence'])

    def __len__(self):
        return len(self.data)

    def __getitem__(self, i):
        return self.data[i]['sentence'], self.data[i]['label']
