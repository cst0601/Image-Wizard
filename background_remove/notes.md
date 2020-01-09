## 16/04/2019
> Midterm

## 09/04/2019
* GitLab repo setup & intro
* Try to run Mask R-CNN on Lab computer (GTX690), **failed**
    * Installed: Mask R-CNN, Tensorflow-1.3, opencv-python
    * When testing with TF, 
        ```bash
            (venv) tars-1422@tars1422-X58A-UD9:~/105820045/Mask_RCNN$ python -c "import tensorflow as tf; f.enable_eager_execution(); print(tf.reduce_sum(tf.random_normal([1000, 1000])))"
            2019-04-09 02:01:27.898877: F tensorflow/core/platform/cpu_feature_guard.cc:37] The TensorFlow library was compiled to use AVX instructions, but these aren't available on your machine.
            已經終止 (core dumped)
        ```
        >   According to [TensorFlow installation guide](https://www.tensorflow.org/install/pip),
            
            Starting with TensorFlow 1.6, binaries use AVX instructions which may not run on older CPUs.



## 02/04/2019
* make slides