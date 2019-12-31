# -*- coding:utf-8 -*-

import time
import argparse
import pickle
import sys, os
import json

sys.path.append(os.getcwd().replace(r"src\dialogue_system\run", ""))

from src.dialogue_system.dialogue_manager import DialogueManager
from src.dialogue_system.agent import AgentRandom
from src.dialogue_system.agent import AgentDQN
from src.dialogue_system.agent import AgentRule
from src.dialogue_system.agent import AgentActorCritic
from src.dialogue_system.user_simulator import UserRule as User
from src.dialogue_system import dialogue_configuration

from src.dialogue_system.run import RunningSteward

# DIR = os.path.abspath('./../') # windows
DIR = os.path.abspath('./') + '/src/dialogue_system/' # Linux
print('DIR is: ', DIR)
device_for_tf = "/device:GPU:10"
disease_number = 5
log_dir = os.path.abspath('./') + "/log/"
performance_save_path = DIR + "model/dqn/learning_rate04/"
checkpoint_path = DIR + "model/dqn/checkpoint/"
dialogue_file = DIR + "data/dialogue_output/dialogue_file.txt"
agent_id = 1
dqn_id = 1
warm_start = 1
explicit_number = 0
implicit_number = 0

# max_turn = 74 * 2


def run_train(simulate_epoch_number, epoch_size, evaluate_epoch_number, hidden_size_dqn, max_turn, reward_for_success,
              reward_for_fail, warm_start_epoch_number, files_index):
    parameter = {}
    parameter['agent_id'] = agent_id
    parameter['dqn_id'] = dqn_id
    parameter['disease_number'] = disease_number
    parameter['device_for_tf'] = device_for_tf
    parameter['log_dir'] = log_dir

    parameter['save_performance'] = 1  # save the performance? 1:Yes, 0:No
    parameter['performance_save_path'] = performance_save_path
    parameter['save_model'] = 1  # save model? 1:Yes,0:No
    parameter[
        'saved_model'] = "./../model/dqn/checkpoint/checkpoint_d5_agt1_dqn2_T66/model_d4_agent1_dqn1_s0.619_r18.221_t4.266_wd0.0_e432.ckpt"
    parameter['checkpoint_path'] = checkpoint_path
    parameter['dialogue_file'] = dialogue_file
    parameter['save_dialogue'] = 1
    parameter['run_id'] = 1
    parameter['explicit_number'] = explicit_number
    parameter['implicit_number'] = implicit_number
    parameter['experience_replay_pool_size'] = 20000
    parameter['allow_wrong_disease'] = 0
    parameter['actor_learning_rate'] = 0.001
    parameter['critic_learning_rate'] = 0.001
    parameter['trajectory_pool_size'] = 48
    parameter['minus_left_slots'] = 0
    if max_turn == 30:
        parameter['input_size_dqn'] = 182
    elif max_turn == 50:
        parameter['input_size_dqn'] = 202
    elif max_turn == 100:
        parameter['input_size_dqn'] = 252
    else:
        parameter['input_size_dqn'] = 302
    data_dir = 'data_' + str(files_index) + '/'
    parameter['action_set'] = DIR + 'data/' + data_dir + 'action_set.p'
    parameter['slot_set'] = DIR + 'data/' + data_dir + 'slot_set.p'
    parameter['goal_set'] = DIR + 'data/' + data_dir + 'goal_set.p'
    parameter['disease_symptom'] = DIR + 'data/' + data_dir + 'disease_symptom.p'

    # setting papameters
    parameter['train_mode'] = 1  # training mode? True:1 or False:0
    parameter['simulate_epoch_number'] = simulate_epoch_number
    parameter['epoch_size'] = epoch_size
    parameter['hidden_size_dqn'] = hidden_size_dqn
    parameter['batch_size'] = 32
    parameter['epsilon'] = 0.1  # the greedy of DQN
    parameter['gamma'] = 0.9  # The discount factor of immediate reward.
    parameter['dqn_learning_rate'] = 0.001
    parameter['max_turn'] = max_turn
    parameter['reward_for_not_come_yet'] = -1
    parameter['reward_for_success'] = reward_for_success * max_turn
    parameter['reward_for_fail'] = - reward_for_fail * max_turn
    parameter['reward_for_inform_right_symptom'] = -1
    parameter['evaluate_epoch_number'] = evaluate_epoch_number
    parameter['warm_start_epoch_number'] = warm_start_epoch_number
    print(json.dumps(parameter, indent=2))
    time.sleep(1)

    print('****************************Run Train***********************************')
    slot_set = pickle.load(file=open(parameter["slot_set"], "rb"))
    action_set = pickle.load(file=open(parameter["action_set"], "rb"))
    disease_symptom = pickle.load(file=open(parameter["disease_symptom"], "rb"))
    steward = RunningSteward(parameter=parameter, checkpoint_path=parameter.get('checkpoint_path'))

    train_mode = parameter.get('train_mode')
    simulate_epoch_number = parameter.get('simulate_epoch_number')
    # Warm start.
    if warm_start == 1 and train_mode == 1:
        print("warm starting...")
        agent = AgentRule(action_set=action_set, slot_set=slot_set, disease_symptom=disease_symptom,
                          parameter=parameter)
        steward.warm_start(agent=agent, epoch_number=parameter.get('warm_start_epoch_number'))
    agent = AgentDQN(action_set=action_set, slot_set=slot_set, disease_symptom=disease_symptom, parameter=parameter)
    # train
    steward.simulate(agent=agent, epoch_number=simulate_epoch_number, train_mode=train_mode)


def run_test(files_index):
    parameter = {}
    parameter['agent_id'] = agent_id
    parameter['dqn_id'] = dqn_id
    parameter['disease_number'] = disease_number
    parameter['device_for_tf'] = device_for_tf
    parameter['log_dir'] = log_dir

    parameter['save_performance'] = 1  # save the performance? 1:Yes, 0:No
    parameter['performance_save_path'] = performance_save_path
    parameter['save_model'] = 1  # save model? 1:Yes,0:No
    parameter[
        'saved_model'] = DIR + "/model/dqn/checkpoint/checkpoint_d5_agt1_dqn2_T66/model_d4_agent1_dqn1_s0.619_r18.221_t4.266_wd0.0_e432.ckpt"
    parameter['checkpoint_path'] = checkpoint_path
    parameter['dialogue_file'] = dialogue_file
    parameter['save_dialogue'] = 1
    parameter['run_id'] = 1
    parameter['explicit_number'] = explicit_number
    parameter['implicit_number'] = implicit_number
    parameter['experience_replay_pool_size'] = 20000
    parameter['allow_wrong_disease'] = 0
    parameter['actor_learning_rate'] = 0.001
    parameter['critic_learning_rate'] = 0.001
    parameter['trajectory_pool_size'] = 48
    parameter['minus_left_slots'] = 0
    if max_turn == 30:
        parameter['input_size_dqn'] = 182
    elif max_turn == 50:
        parameter['input_size_dqn'] = 202
    elif max_turn == 100:
        parameter['input_size_dqn'] = 252
    else:
        parameter['input_size_dqn'] = 302
    data_dir = 'data_' + str(files_index) + '/'
    parameter['action_set'] = DIR + 'data/' + data_dir + 'action_set.p'
    parameter['slot_set'] = DIR + 'data/' + data_dir + 'slot_set.p'
    parameter['goal_set'] = DIR + 'data/' + data_dir + 'goal_set.p'
    parameter['disease_symptom'] = DIR + 'data/' + data_dir + 'disease_symptom.p'

    # setting papameters
    parameter['train_mode'] = 0  # training mode? True:1 or False:0
    parameter['simulate_epoch_number'] = 1
    parameter['epoch_size'] = 50
    parameter['hidden_size_dqn'] = 64
    parameter['batch_size'] = 32
    parameter['epsilon'] = 0.1  # the greedy of DQN
    parameter['gamma'] = 0.9  # The discount factor of immediate reward.
    parameter['dqn_learning_rate'] = 0.001
    parameter['max_turn'] = max_turn
    parameter['reward_for_not_come_yet'] = -1
    parameter['reward_for_success'] = 2.0 * max_turn
    parameter['reward_for_fail'] = -2.0 * max_turn
    parameter['reward_for_inform_right_symptom'] = -1
    parameter['evaluate_epoch_number'] = 100
    print(json.dumps(parameter, indent=2))
    time.sleep(1)

    print('*************************Run Test**************************************')
    slot_set = pickle.load(file=open(parameter["slot_set"], "rb"))
    action_set = pickle.load(file=open(parameter["action_set"], "rb"))
    disease_symptom = pickle.load(file=open(parameter["disease_symptom"], "rb"))
    steward = RunningSteward(parameter=parameter, checkpoint_path=checkpoint_path)

    train_mode = parameter.get('train_mode')
    simulate_epoch_number = parameter.get('simulate_epoch_number')
    agent = AgentDQN(action_set=action_set, slot_set=slot_set, disease_symptom=disease_symptom, parameter=parameter)
    # test
    steward.simulate(agent=agent, epoch_number=simulate_epoch_number, train_mode=train_mode)


if __name__ == "__main__":
    # setting 由于是单线程的，实际运行的时候可以拆分参数，同时跑几个实验。
    experment_num = 10
    evaluate_epoch_number = 100
    epoch_size = 100
    warm_start_epoch_number = 200
    for simulate_epoch_number in [100, 200, 500, 1000]:
        for hidden_size_dqn in [256, 128, 64, 32, 16, 8]:
            for reward_for_fail in [1.0, 2.0, 3.0, 4.0]:
                for reward_for_success in [1.0, 2.0, 3.0, 4.0]:
                    for max_turn in [30, 50, 100, 150]:
                        with open(DIR + 'data/test.txt', 'a') as f:  # 设置文件对象
                            f.write(
                                'Paramaters: ' + str(evaluate_epoch_number) + ', ' + str(epoch_size) + ', ' + str(
                                    warm_start_epoch_number) + ',| ' + str(hidden_size_dqn) + ', ' + str(
                                    reward_for_fail) + ', ' + str(
                                    simulate_epoch_number) + ', ' + str(reward_for_success) + ', ' + str(
                                    max_turn) + '\n')
                            f.close()
                            for i in range(experment_num):
                                time_start = time.time()
                                run_train(simulate_epoch_number, epoch_size, evaluate_epoch_number,
                                          hidden_size_dqn, max_turn,
                                          reward_for_success, reward_for_fail, warm_start_epoch_number, i)
                                run_test(i)
                                print('第%s次实验全部结束----------------------' % str(i + 1))
                                time_end = time.time()
                                print('totally cost', time_end - time_start, '平均每轮耗时',
                                      (time_end - time_start) / 10)