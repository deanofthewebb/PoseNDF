import argparse
from configs.config import load_config
# General config

#from model_quat import  train_manifold2 as train_manifold
from model import train_posendf  as PoseNDF_trainer
from model import load_data
import shutil
from data.data_splits import amass_splits

def train(opt,config_file):

    trainer = PoseNDF_trainer(opt)
    # copy the config file
    copy_config = '{}/{}/{}'.format(opt['experiment']['root_dir'], trainer.exp_name, 'config.yaml')
    shutil.copyfile(config_file,copy_config )
    val = opt['experiment']['val']
    test = opt['experiment']['test']
    if test:
        trainer.inference(trainer.ep)
    for i in range(trainer.ep, opt['train']['max_epoch']):
        loss,epoch_loss = trainer.train_model(i)
        if val and i%100==0:
            trainer.validate(i)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Train PoseNDF.'
    )
    parser.add_argument('--config', '-c', default='configs/amass.yaml', type=str, help='Path to config file.')
    args = parser.parse_args()

    opt = load_config(args.config)
    #save the config file

    train(opt, args.config)