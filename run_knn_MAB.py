import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import networkx as nx 
import os
os.chdir('C:/Kaige_Research/Graph Learning/graph_learning_code/')
from collections import Counter
import datetime
from synthetic_data import *
from gl_MAB import GL_MAB
from knn_MAB import KNN_MAB
from correct_knn_MAB import Correct_KNN_MAB
from cd_MAB import CD_MAB
from linucb_MAB import LINUCB_MAB
from sklearn.metrics.pairwise import rbf_kernel
path='C:/Kaige_Research/Graph Learning/graph_learning_code/results/MAB_models_results/'
timeRun = datetime.datetime.now().strftime('_%m_%d_%H_%M_%S') 

user_num=50
item_num=1000
dimension=10
item_pool_size=5
cluster_num=4
cluster_std=0.25
noise_scale=0.25
K=user_num
gl_alpha=1
gl_beta=0.2
gl_theta=0.01
gl_step_size=0.5
alpha=0.05
iteration=10000

newpath=path+'KNN_user_num_%s_cluster_num_%s'%(user_num, cluster_num)+'/'+str(timeRun)+'/'
if not os.path.exists(newpath):
	    os.makedirs(newpath)

user_pool=generate_all_random_users(iteration, user_num)
item_pools=generate_all_article_pool(iteration, item_pool_size, item_num)


noisy_signal, true_signal, item_features, true_user_features, true_label=blob_data(user_num, item_num, dimension, cluster_num, cluster_std, noise_scale)
true_adj=rbf_kernel(true_user_features)
np.fill_diagonal(true_adj,0)


knn_mab=KNN_MAB(user_num, item_num, dimension, item_pool_size,alpha, K=K,  true_user_features=true_user_features, true_graph=true_adj)
knn_cum_regret, knn_adj,knn_user_f, knn_error,knn_graph_error, knn_denoised_signal=knn_mab.run(user_pool, item_pools, item_features, noisy_signal,true_signal, iteration)

knn_mab_2=KNN_MAB(user_num, item_num, dimension, item_pool_size,alpha, K=K, true_user_features=true_user_features, true_graph=true_adj)
knn_cum_regret_2, knn_adj_2,knn_user_f_2, knn_error_2,knn_graph_error_2, knn_denoised_signal_2=knn_mab_2.run(user_pool, item_pools, item_features, noisy_signal, true_signal, iteration)

c_knn_mab=Correct_KNN_MAB(user_num, item_num, dimension, item_pool_size,alpha, K=K, true_user_features=true_user_features, true_graph=true_adj)
c_knn_cum_regret, c_knn_adj,c_knn_user_f, c_knn_error,c_knn_graph_error, c_knn_denoised_signal=c_knn_mab.run(user_pool, item_pools, item_features, noisy_signal, true_signal, iteration)

plt.plot(knn_cum_regret, label='KNN_1')
plt.plot(knn_cum_regret_2, label='KNN_2')
plt.plot(c_knn_cum_regret, label='KNN_c')
plt.ylabel('Cum Regret', fontsize=12)
plt.legend(loc=1)
plt.show()

plt.plot(knn_error, label='KNN_1')
plt.plot(knn_error_2, label='KNN_2')
plt.plot(c_knn_error, label='KNN_c')
plt.ylabel('Learning Error', fontsize=12)
plt.legend(loc=1)
plt.show()



pos=true_user_features
graph=create_networkx_graph(user_num, true_adj)
edge_color=true_adj[np.triu_indices(user_num,1)]
plt.figure(figsize=(5,5))
nodes=nx.draw_networkx_nodes(graph, pos, node_color=noisy_signal[0], node_size=100, cmap=plt.cm.jet)
edges=nx.draw_networkx_edges(graph, pos, width=1.0, alpha=0.1, edge_color='grey')
plt.axis('off')
plt.title('True Graph', fontsize=12)
plt.show()




pos=true_user_features
graph=create_networkx_graph(user_num, knn_adj)
edge_color=knn_adj[np.triu_indices(user_num,1)]
plt.figure(figsize=(5,5))
nodes=nx.draw_networkx_nodes(graph, pos, node_color=knn_denoised_signal[0], node_size=100, cmap=plt.cm.jet)
edges=nx.draw_networkx_edges(graph, pos, width=1.0, alpha=0.1, edge_color='grey')
plt.axis('off')
plt.title('KNN Graph', fontsize=12)
plt.show()




fig, (ax1, ax2)=plt.subplots(1,2, figsize=(6,3))
ax1.scatter(pos[:,0], pos[:,1], c=noisy_signal[0].tolist(), cmap=plt.cm.jet)
ax2.scatter(pos[:,0], pos[:,1], c=knn_denoised_signal[0].tolist(), cmap=plt.cm.jet)
ax1.axis('off')
ax2.axis('off')
ax1.set_title('Noisy Signal')
ax2.set_title('KNN Signal')
plt.tight_layout()
plt.show()

