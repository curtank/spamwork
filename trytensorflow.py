import generatelabels
import tensorflow as tf
import numpy as np 
import pickle 
import os
bucketlen=500
def gotone():
    rootdir='./wordCHIbucket'
    labels=generatelabels.getlabels()
    #print labels
    #print labels['/136/136']
    
    for parent,dirnames,filenames in os.walk(rootdir):
        for filename in filenames:
            fullname=parent+'/'+filename
            #print(fullname)
            index=parent[-4:]+'/'+filename
            #print(index)
            f=open(fullname,'rb')
            bucket=pickle.load(open(fullname,'rb'),)
            
            x=np.array(bucket[0:bucketlen])
            y=np.array(labels[index])
            
            #print x
            #print np.sum(x)
            yield x,y
def gotfakedata():
    i=0
    while True:
        x=np.random.rand(1)
        y=x*3+2
        yield x,y[0]
g=gotone()
#g=gotfakedata()
def gotpatch(num):
    xs=[]
    ys=[]
    for i in range(num):
        x,y=g.next()
        xs.append(x)
        ys.append([y])

    #print np.sum(ys)
    return xs, ys
def main():
    
    
    num=1
    hw=1
    with tf.name_scope('input'):
        x=tf.placeholder(tf.float32,[None,bucketlen])
        y_=tf.placeholder(tf.float32,[None,1])
    with tf.name_scope('weight'):
        W=tf.Variable(tf.random_uniform([bucketlen,hw],minval=-10,maxval=10))
    with tf.name_scope('biases'):
        b=tf.Variable(tf.random_uniform([hw],maxval=10))
    
 #   with tf.name_scope('hidden'):
#        hW=tf.Variable(tf.random_uniform([hw,1],maxval=10))
#        hb=tf.Variable(tf.random_uniform([1],maxval=10))
#        h=tf.matmul(x,W)+b
#    with tf.name_scope('out'):
        #y=tf.sigmoid(tf.matmul(h,hW)+hb)
        y=tf.sigmoid(tf.matmul(x,W))
    
    
    print x,W,b,y,y_
    with tf.name_scope('cross'):
        diff=tf.square(y-y_)
        cross_entropy =tf.reduce_mean(diff)+tf.reduce_mean(tf.square(W))*0.005
    
    train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)
    with tf.name_scope('change'):
        tf.summary.scalar('cross',cross_entropy)
        tf.summary.scalar('Wchange',tf.reduce_mean(tf.square(W)))
        tf.summary.scalar('b',tf.reduce_mean(b))
        tf.summary.scalar('y',tf.reduce_sum(y))
        tf.summary.scalar('y_',tf.reduce_sum(y_))
        tf.summary.scalar('diff',tf.reduce_mean(tf.abs(y-y_)))
 #   with tf.name_scope('hidden'):
 #       tf.summary.scalar('hw',tf.reduce_mean(hW))
 #      tf.summary.scalar('hb',tf.reduce_mean(hb))
    #print cross_entropy
    sess = tf.InteractiveSession()
    merged=tf.summary.merge_all()
    summary_writer = tf.summary.FileWriter('./logs', sess.graph)
    tf.global_variables_initializer().run()

    for i in range(20000):
        batch_xs,batch_ys=gotpatch(num)
        sess.run([train_step],feed_dict={x:batch_xs,y_:batch_ys})
        #batch_x,batch_y=gotpatch(1)
        if i%10==0:
            summary,=sess.run([merged],feed_dict={x:batch_xs,y_:batch_ys})
            summary_writer.add_summary(summary,global_step=i)
            print i
        
        #correct_prediction = tf.equal(tf.argmin(y, 1), tf.argmin(y_, 1))
    
    #accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    

if __name__ == '__main__':
    main()
    