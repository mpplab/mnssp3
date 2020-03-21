<?php

namespace app\index\controller;

use think\Controller;
use think\Db;

class Drd extends Controller
{
    public function rundrd($img_path=null)
    {
        if (!$img_path) {
            $data = array('code' => 0, 'msg' => 'fail', 'data' => '参数错误');
            echo json_encode($data);
        } else {
            $output = exec("python3 Python/Diabetic_Retinopathy_Detection/test.py {$img_path} 2>&1", $out, $status);
            if ($status > 0) {
                $data = array('code' => 0, 'msg' => 'fail', 'data' => '系统繁忙');
                echo json_encode($data);
            } else {
                $data = array('code' => 1, 'msg' => 'success', 'data' => $output);
                echo json_encode($data);
            }
        }
    }
}
