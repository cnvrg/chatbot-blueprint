# Copyright (c) 2022 Intel Corporation
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# SPDX-License-Identifier: MIT

import requests
import os
import pathlib


def download_model_files():
    current_dir = pathlib.Path(__file__).parent.resolve()
    if not os.path.exists(str(current_dir) + '/chatbot_model.pt') and not os.path.exists('/input/train/chatbot_model.pt'):
        MODEL_FILE_URL = "https://blueprints-data.s3.us-west-2.amazonaws.com/model_files/chatbot/chatbot_model.pt"
        print('Downloading Model Files...')
        response = requests.get(MODEL_FILE_URL)
        open("chatbot_model.pt", "wb").write(response.content)
        print('Model Files Downloaded!')
