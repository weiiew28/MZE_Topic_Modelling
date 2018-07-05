import os
import csv
trials = 5

os.system(r'mallet import-dir --input /Users/Wei/Documents/Technique_Study/Coding/LeetCode/MZE/Data/Corpus/Train --output /Users/Wei/Documents/Technique_Study/Coding/LeetCode/MZE/Data/mze_train.mallet --stoplist-file /Users/Wei/Documents/Technique_Study/Coding/LeetCode/MZE/Data/de_stop_addstem.txt --keep-sequence')

os.system(r'mallet import-dir --input /Users/Wei/Documents/Technique_Study/Coding/LeetCode/MZE/Data/Corpus/Test --output /Users/Wei/Documents/Technique_Study/Coding/LeetCode/MZE/Data/mze_test.mallet --stoplist-file /Users/Wei/Documents/Technique_Study/Coding/LeetCode/MZE/Data/de_stop_addstem.txt --keep-sequence')

alphas = [1.0,2.0]
betas = [0.001,0.01,0.1,1]
K = [50,100]
iterations = [1000,4000]


prob_evaluate_file = open('/Users/Wei/Documents/Technique_Study/Coding/LeetCode/MZE/Data/mze_experiment_prob.csv','w')
prob_evaluate = csv.writer(prob_evaluate_file)
prob_evaluate.writerow(['num_topic','alpha','beta','iter','trial1','trial2','trial3','trial4','trial5'])
for alpha in alphas:
    for beta in betas:
        for topic_num in K:
            for iteration in iterations:
                trial_result = []
                for trial in range(trials):
                    os.system(r'mallet train-topics --input /Users/Wei/Documents/Technique_Study/Coding/LeetCode/MZE/Data/mze_train.mallet --evaluator-filename /Users/Wei/Documents/Technique_Study/Coding/LeetCode/MZE/Data/mze_evaluate --num-topics {0} --num-iterations {1} --alpha {2} --beta {3}'.format(topic_num,iteration,alpha,beta))
                    os.system('mallet evaluate-topics --evaluator /Users/Wei/Documents/Technique_Study/Coding/LeetCode/MZE/Data/mze_evaluate --input /Users/Wei/Documents/Technique_Study/Coding/LeetCode/MZE/Data/mze_test.mallet --use-resampling --num-iterations 200 --burn-in 20 --output-prob /Users/Wei/Documents/Technique_Study/Coding/LeetCode/MZE/Data/mze_test_prob')
                    g = open('/Users/Wei/Documents/Technique_Study/Coding/LeetCode/MZE/Data/mze_test_prob','r')
                    log_prob = float(g.readline())
                    trial_result.append(log_prob)
                    g.close()
                prob_evaluate.writerow([topic_num,alpha,beta,iteration]+trial_result)
prob_evaluate_file.close()

