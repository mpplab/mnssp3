<?php

namespace app\index\controller;

use think\Controller;
use think\Db;

class Ed extends Controller
{
    public function savejilu()
    {
        $user = Db::name('user')->where(array('id' => $uid, 'isdel' => 0))->find();
        $post = $_POST['data'];
        if ((!isset($post['filename']))  && (!isset($post['filerename']))) {
            $data = array('code' => 0, 'msg' => 'fail', 'data' => '参数错误');
            echo json_encode($data);
            return;
        }
        $filename = '';
        $filerename = '';
        $filesrc = '';
        $xulie = '';
        if (!empty($post['filename'])) {
            $filename = $post['filename'];
            $filesrc = $post['filesrc'];
            $filerename = $post['filerename'];
        } else {
            $data = array('code' => 0, 'msg' => 'fail', 'data' => '未上传文件');
            echo json_encode($data);
            return;
        }
        $jilu = array(
            'userid' => $uid,
            'username' => $user['username'],
            'filename' => $filename,
            'filerename' => $filerename,
            'stysrc' => '/EEG/data/upload/',
            'filesrc' => $filesrc,
            'create_time' => time(),
        );
        $path = '/Python/EEG/data/upload'.$filesrc;
        if(empty($post['mo'])){
            $exec = "python3 Python/EEG/predict.py {$path} 2>&1";
        }else{
            $mo_filesrc = $user['mo_filesrc'];
            $jilu['mo_filerename']=$user['mo_filerename'];
            $exec = "python3 Python/EEG/predict.py {$path} {$mo_filesrc} 2>&1";
        }
        $output = exec($exec, $out, $status);
        // echo $output
        if ($status > 0) {
            $data = array('code' => 0, 'msg' => 'fail', 'data' => 'The system is busy, please try again later');
            echo json_encode($data);
            return;
        } else {
            $data = array('code' => 1, 'msg' => 'success', 'data' => $output);
            $jilu['output']=$output;
            $jilu_id = Db::name('ed_jilu')->insertGetId($jilu);
            if ($jilu_id > 0) { 
                $data = array('code' => 1, 'msg' => 'success', 'data' => $output);
            } else {
                $data = array('code' => 0, 'msg' => 'fail', 'data' => 'The system is busy, please try again later');
                echo json_encode($data);
                return;
            }
            echo json_encode($data);
            return;
        }
        
        
    }

    

    

   
    
}
