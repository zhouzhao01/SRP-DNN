""" 
    Function:   Define some optional arguments and configurations
"""

import argparse
import time
import os

class opt():
    def __init__(self):
        time_stamp = time.time()
        local_time = time.localtime(time_stamp)
        self.time = time.strftime('%m%d%H%M', local_time)
        
    def parse(self):
        """ Function: Define optional arguments
        """
        parser = argparse.ArgumentParser(description='Self-supervised learing for multi-channel audio processing')

        # for both training and test stages
        parser.add_argument('--gpu-id', type=str, default='7', metavar='GPU', help='GPU ID (default: 7)')
        parser.add_argument('--workers', type=int, default=0, metavar='Worker', help='number of workers (default: 0)')
        parser.add_argument('--no-cuda', action='store_true', default=False, help='disables CUDA training (default: False)')
        parser.add_argument('--use-amp', action='store_true', default=False, help='Use automatic mixed precision training (default: False)')
        parser.add_argument('--seed', type=int, default=1, metavar='Seed', help='random seed (default: 1)')
        parser.add_argument('--train', action='store_true', default=False, help='change to train stage (default: False)')
        parser.add_argument('--test', action='store_true', default=False, help='change to test stage (default: False)')
        parser.add_argument('--checkpoint-start', action='store_true', default=False, help='train model from saved checkpoints (default: False)')
        parser.add_argument('--time', type=str, default=self.time, metavar='Time', help='time flag')
    
        parser.add_argument('--sources', type=int, nargs='+', default=[1,2], metavar='Sources', help='Number of sources (default: 1, 2)')
        parser.add_argument('--source-state', type=str, default='mobile', metavar='SourceState', help='State of sources (default: Mobile)')
        parser.add_argument('--localize-mode', type=str, nargs='+', default=['IDL','unkNum', 2], metavar='LocalizeMode', help='Mode for localization (default: Iterative detection and localization method, Unknown source number, Maximum source number is 2)')
        # e.g., ['IDL','unkNum', 2], ['IDL','kNum', 1], ['PD','kNum', 1]
        parser.add_argument('--eval-mode', type=str, nargs='+', default=['locata', 'pred', 'eval'], metavar='EvaluationMode', help='Mode for evaluation (default: LOCATA dataset, Predcition, Evaluation)')
        # e.g., ['locata','pred'], ['locata','eval'], ['simulate', 'all'], ['simulate', 'some']
        # parser.add_argument('--array', type=str, default='12ch', metavar='ArrayType', help='Type of microphone array (default: 12ch)')

        # for training stage
        parser.add_argument('--bz', type=int, nargs='+', default=[1,1,1], metavar='TrainValTestBatch', help='batch size for training, validation and test (default: 1, 1, 5)')
        parser.add_argument('--epochs', type=int, default=18, metavar='Epoch', help='number of epochs to train (default: 18)')
        parser.add_argument('--lr', type=float, default=0.001, metavar='LR', help='learning rate (default:0.001)')
                   
        args = parser.parse_args()
        self.time = args.time

        if (args.train + args.test)!=1:
            raise Exception('Stage of train or test is unrecognized')

        return args
        
    def dir(self):
        """ Function: Get directories of code, data and experimental results
        """ 
        work_dir = r'~'
        work_dir = os.path.abspath(os.path.expanduser(work_dir))
        dirs = {}

        dirs['code'] = work_dir + '/SRP-DNN/code'
        dirs['data'] = work_dir + '/SRP-DNN/data'
        # dirs['data'] = work_dir + '/data'
        dirs['gerdata'] = work_dir + '/SRP-DNN/data'
        dirs['exp'] = work_dir + '/SRP-DNN/exp'

        # signal data
        dirs['sousig_train'] = dirs['data'] + '/SouSig/LibriSpeech/train-clean-100'
        dirs['sousig_val'] = dirs['data'] + '/SouSig/LibriSpeech/dev-clean'
        dirs['sousig_test'] = dirs['data'] + '/SouSig/LibriSpeech/test-clean'
        dirs['sensig_locata'] = dirs['data'] + '/SenSig/LOCATA'
        # dirs['noisig_train'] = dirs['data'] + '/NoiSig/NOISEX-92'
        # dirs['noisig_val'] = dirs['data'] + '/NoiSig/NOISEX-92'
        # dirs['noisig_test'] = dirs['data'] + '/NoiSig/NOISEX-92'

        # experimental data
        dirs['log'] = dirs['exp'] + '/' + self.time

        return dirs

if __name__ == '__main__':
    opts = opt()
    args = opts().parse()
    dirs = opts().dir()