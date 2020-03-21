<?php

namespace app\index\controller;

use think\Controller;
use think\Db;

class Sim extends Controller
{
    public function content()
    {
        if (!isset($_GET['id'])) {
            echo 'fail';
            return;
        }
        $id = $_GET['id'];
        $jindu = Db::name('jindu')->where(array('id' => $id, 'isdel' => 0))->find();
        if (!$jindu) {
            echo 'fail';
            return;
        }
        $ngramlist = array();
        $gibbsjieguo = '';
        if ($jindu['fangfa'] == 'n-gram') {

            $file_path = '.' . $jindu['output_filesrc'] . $jindu['output_filename'];
            if (file_exists($file_path)) {
                $file = fopen($file_path, "r") or exit("Unable to open file!");
                while (!feof($file)) {
                    $hang = fgets($file);
                    $res = explode(':', $hang);
                    if (count($res) < 2) {
                        break;
                    }
                    $Motif = $res[0];
                    $Count = preg_replace("/\r\n/", '', $res[1]);
                    array_push($ngramlist, array('Motif' => $Motif, 'Count' => $Count));
                }
                fclose($file);
            }
        } elseif ($jindu['fangfa'] == 'gibbs') {
            $file_path = '.' . $jindu['output_filesrc'] . $jindu['output_filename'] . '-predictedmotif.txt';
            if (file_exists($file_path)) {
                $handle = fopen($file_path, "r");
                $contents = fread($handle, filesize($file_path));
                $contents = preg_replace("/\\d+/", '', $contents);
                $contents = preg_replace("/\\t/", '', $contents);
                $contents = preg_replace("/\\n/", '', $contents);
                $contents = $this->cut('>', '<', $contents);
                $gibbsjieguo = $contents;
                fclose($handle);
            }
        }
        $date = date('Y-m-d H:m:s', $jindu['create_time']);
        $res = [
            'create_time' => $date,
            'filerename' => $jindu['filerename'],
            'fangfa' => $jindu['fangfa'],
            'L_Left' => $jindu['L_Left']== 0 ? 'none' : $jindu['L_Left'],
            'theta' => $jindu['theta'] == 0 ? 'none' : $jindu['theta'],
            'epsilon' => $jindu['epsilon'] == 0 ? 'none' : $jindu['epsilon'],
            'ngramlist' => $ngramlist ? $ngramlist : '',
            'hidden_jieguo' => $jindu['fangfa'] == 'n-gram' ? '' : 'hidden',
            'gibbsjieguo' => $gibbsjieguo,
            'hidden_gibbs' => $jindu['fangfa'] == 'gibbs' ? '' : 'hidden',
            'gotoid'=>$jindu['id'],
            'hidden_logo' => $jindu['fangfa'] == 'logo' ? '' : 'hidden',
            'display_logo' => $jindu['fangfa'] == 'logo' ? 'none' : '',

        ];
        return view('content', $res);
    }

    public function getfun_jilu()
    {
        $count = Db::name('upload_fun')->where(array('userid' => $uid, 'isdel' => 0))->count();
        $upload_funlist = Db::name('upload_fun')->where(array('userid' => $uid, 'isdel' => 0))->order('create_time desc,id desc')->page($_GET['page'] . ',' . $_GET['limit'])->select();
        $res = array('code' => 0, 'data' => $upload_funlist, 'count' => $count);
        echo json_encode($res);
        return;
    }
    public function sch()
    {
        return json_encode(file_exists('./Python/n-gram/simple/data/input/'));
    }
    public function getjilu()
    {
        $count = Db::name('jindu')->where(array('userid' => $uid, 'isdel' => 0))->count();
        $jindulist = Db::name('jindu')->where(array('userid' => $uid, 'isdel' => 0))->order('create_time desc,id desc')->page($_GET['page'] . ',' . $_GET['limit'])->select();
        $jindulist_runing = Db::name('jindu')->where(array('userid' => $uid, 'isdel' => 0, 'state' => 1))->select();
        $res = array('code' => 0, 'data' => $jindulist, 'count' => $count);
        foreach ($jindulist_runing as $value) {
            if ($value['fangfa'] === 'n-gram') {
                if (file_exists('.' . $value['output_filesrc'] . $value['output_filename'])) {
                    Db::name('jindu')->where(array('id' => $value['id'], 'isdel' => 0))->update(['state' => 2]);
                } else {
                    if ((time() - $value['run_time']) > 86400) {
                        Db::name('jindu')->where(array('id' => $value['id'], 'isdel' => 0))->update(['state' => 3]);
                    }
                }
            } else if ($value['fangfa'] === 'gibbs') {
                if (file_exists('.' . $value['output_filesrc'] . $value['output_filename'] . '-IC.npy')) {
                    Db::name('jindu')->where(array('id' => $value['id'], 'isdel' => 0))->update(['state' => 2]);
                } else {
                    if ((time() - $value['run_time']) > 86400) {
                        Db::name('jindu')->where(array('id' => $value['id'], 'isdel' => 0))->update(['state' => 3]);
                    }
                }
            }else if ($value['fangfa'] === 'logo') {
                if (file_exists('.' . $value['output_filesrc'] . $value['output_filename'])) { 
                    Db::name('jindu')->where(array('id' => $value['id'], 'isdel' => 0))->update(['state' => 2]);
                } else {
                    if ((time() - $value['run_time']) > 86400) {
                        Db::name('jindu')->where(array('id' => $value['id'], 'isdel' => 0))->update(['state' => 3]);
                    }
                }
            }
        }
        echo json_encode($res);
        return;
    }

    public function saveuploadfun()
    {
        $user = Db::name('user')->where(array('id' => $uid, 'isdel' => 0))->find();
        $post = $_POST['data'];
        if ((!isset($post['fwq'])) || (!isset($post['python'])) || (!isset($post['filename']))) {
            $data = array('code' => 0, 'msg' => 'fail', 'data' => '参数错误');
            echo json_encode($data);
            return;
        }
        $filename = '';
        $filerename = '';
        $filesrc = '';
        if (!empty($post['filename'])) {
            $filename = $post['filename'];
            $filesrc = $post['filesrc'];
            $filerename = $post['filerename'];
        } else {
            $data = array('code' => 0, 'msg' => 'fail', 'data' => '未上传序列文件');
            echo json_encode($data);
            return;
        }
        $fwq = $post['fwq'];
        $python = $post['python'];
        $upload_fun = array(
            'userid' => $uid,
            'username' => $user['username'],
            'fwq' => $fwq,
            'python' => $python,
            'filename' => $filename,
            'filerename' => $filerename,
            'stysrc' => "/upload_fun/",
            'filesrc' => $filesrc,
            'state' => 0,
            'create_time' => time(),
        );
        $upload_fun_id = Db::name('upload_fun')->insertGetId($upload_fun);

        if ($upload_fun_id > 0) {
            $data = array('code' => 1, 'msg' => 'success', 'data' => $upload_fun_id);
            echo json_encode($data);
            return;
        } else {
            $data = array('code' => 0, 'msg' => 'fail', 'data' => '系统繁忙');
            echo json_encode($data);
            return;
        }
        echo json_encode($post);
        return;
    }


    public function savejilu()
    {
        $user = Db::name('user')->where(array('id' => $uid, 'isdel' => 0))->find();
        $post = $_POST['data'];
        // return json_encode($post);
        if ((!isset($post['fangfa'])) || (!isset($post['L_Left'])) || (!isset($post['theta'])) || (!isset($post['epsilon']))) {
            $data = array('code' => 0, 'msg' => 'fail', 'data' => '参数错误');
            echo json_encode($data);
            return;
        }
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
            $data = array('code' => 0, 'msg' => 'fail', 'data' => '未上传序列文件');
            echo json_encode($data);
            return;
        }
        // if (isset($post['xulie'])) {
        //     $xulie = $post['xulie'];
        // }
        $fangfa = $post['fangfa'];
        $L_Left = $post['L_Left'];
        $theta = $post['theta'];
        $epsilon = $post['epsilon'];
        $jindu = array(
            'userid' => $uid,
            'username' => $user['username'],
            'fangfa' => $fangfa,
            'L_Left' => $L_Left,
            'theta' => $theta,
            'epsilon' => $epsilon,
            'filename' => $filename,
            'filerename' => $filerename,
            'stysrc' => '/Python/n-gram/simple/data/input/',
            'filesrc' => $filesrc,
            // 'xulie' => $xulie,
            'state' => 0,
            'create_time' => time(),
        );
        $jindu_id = Db::name('jindu')->insertGetId($jindu);
        if ($jindu_id > 0) {
            $data = array('code' => 1, 'msg' => 'success', 'data' => $jindu_id);
            echo json_encode($data);
            return;
        } else {
            $data = array('code' => 0, 'msg' => 'fail', 'data' => '系统繁忙');
            echo json_encode($data);
            return;
        }
    }

    public function runsim()
    {
        $post = $_POST;
        if ((!isset($post['id']))) {
            $data = array('code' => 0, 'msg' => 'fail', 'data' => '参数错误');
            echo json_encode($data);
            return;
        }
        $id = $post['id'];
        $jindu = Db::name('jindu')->where(array('id' => $id, 'isdel' => 0))->find();
        if (!$jindu) {
            $data = array('code' => 0, 'msg' => 'fail', 'data' => '参数错误');
            echo json_encode($data);
            return;
        }
        $output_filename = md5(uniqid());
        $output_filename_gibbs = $output_filename;

        $L_Left = $jindu['L_Left'];
        $epsilon = $jindu['epsilon'];
        $theta = $jindu['theta'];
        $filename = $jindu['userid'] . '\\' . $jindu['filename'];
        // echo json_encode($filename);
        // return; 
        if ($jindu['fangfa'] === 'n-gram') {
            $res = Db::name('jindu')->where(array('id' => $id, 'isdel' => 0))->update(['state' => 1, 'output_filename' => $output_filename . '.fa', 'run_time' => time(), 'output_filesrc' => '/simple/MNSS/result/']);
        } else if ($jindu['fangfa'] === 'gibbs') {
            $res = Db::name('jindu')->where(array('id' => $id, 'isdel' => 0))->update(['state' => 1, 'output_filename' => $output_filename, 'run_time' => time(), 'output_filesrc' => '/motifFinding-master-4/MNSS/result/' . $uid . '/' . $output_filename . '/']);
        }else if ($jindu['fangfa'] === 'logo') {
            $res = Db::name('jindu')->where(array('id' => $id, 'isdel' => 0))->update(['state' => 1, 'output_filename' => $output_filename . '.png', 'run_time' => time(), 'output_filesrc' => '/MNSS3/MNSS/result/']);
        }
       
        if ($res > 0) {
            $data = array('code' => 1, 'msg' => 'success', 'data' => $res);
            set_time_limit(0);
            ob_end_clean();
            header("Connection: close");
            header("HTTP/1.1 200 OK");
            header("Content-Type: application/json;charset=utf-8"); // 如果前端要的是json则添加，默认是返回的html/text
            ob_start();
            echo json_encode($data); // 输出结果到前端
            $size = ob_get_length();
            header("Content-Length: $size");
            ob_end_flush();
            flush();
            if (function_exists("fastcgi_finish_request")) { // yii或yaf默认不会立即输出，加上此句即可（前提是用的fpm）
                fastcgi_finish_request(); // 响应完成, 立即返回到前端,关闭连接
            }
            sleep(2);
            ignore_user_abort(true); // 在关闭连接后，继续运行php脚本
            set_time_limit(0);
        } else {
            $data = array('code' => 0, 'msg' => 'fail', 'data' => '系统繁忙');
            echo json_encode($data);
            return;
        }
        if ($jindu['fangfa'] === 'n-gram') {
            exec("python2 Python/n-gram/simple/simple.py {$output_filename} {$L_Left} {$epsilon} {$theta} {$filename} 2>&1", $out, $res);
        } else if ($jindu['fangfa'] === 'gibbs') {
            $output_filename = 'Python/gibbs/motifFinding-master-4/MNSS/result/' . $uid . '/' . $output_filename . '/' . $output_filename;
            $filename = '/Python/n-gram/simple/data/input/' . $filename;
            $path = './Python/gibbs/motifFinding-master-4/MNSS/result/' . $uid . '/' . $output_filename_gibbs . '/';
            if (!file_exists($path)) {
                mkdir($path, 0700, true);
            }
            exec("python2 Python/gibbs/motifFinding-master-4/gibbs.py {$output_filename} {$L_Left} {$filename} 2>&1", $out, $res);
        }else if ($jindu['fangfa'] === 'logo') {
            
            $filename = '/Python/n-gram/simple/data/input/' . $filename;
            exec("python3 Python/logo/logo.py {$output_filename} {$filename} 2>&1", $out, $res);
        }
    }  

    public function down()
    {
        if ((!isset($_GET['id']))) {
            $data = array('code' => 0, 'msg' => 'fail', 'data' => '参数错误');
            echo json_encode($data);
            return;
        }

        $id = $_GET['id'];
        $jindu = Db::name('jindu')->where(array('id' => $id, 'isdel' => 0))->find();
        if (!$jindu) {
            echo '错误文件';
            return;
        }
        if ($jindu['fangfa'] === 'n-gram') {

            $file = '.' . $jindu['output_filesrc'] . $jindu['output_filename'];   //文件路径

            $filename = basename($file); //要下载文件的名字

            header("Content-Type: application/force-download");

            header("Content-Disposition: attachment; filename=" . ($filename));

            readfile($file);
            exit();
        } else if ($jindu['fangfa'] === 'gibbs') {
            $path = '.' . $jindu['output_filesrc'];
            $filename = '.' . $jindu['output_filesrc'] . $jindu['output_filename'] . '.zip';
            if (!file_exists($filename)) {
                $this->z_zipdir($path, $filename);
            }
            header("Cache-Control: public");
            header("Content-Description: File Transfer");
            header('Content-disposition: attachment; filename=' . basename($filename)); //文件名
            header("Content-Type: application/zip"); //zip格式的
            header("Content-Transfer-Encoding: binary"); //告诉浏览器，这是二进制文件
            header('Content-Length: ' . filesize($filename)); //告诉浏览器，文件大小
            readfile($filename);
            exit();
        }
    }

    public function z_addDir2Zip($dir, $zip)
    {
        $handler = opendir($dir);
        while (($filename = readdir($handler)) !== false) {
            if ($filename != "." && $filename != "..") {
                if (is_dir($dir . '/' . $filename)) {
                    $this->z_addDir2Zip($dir . "/" . $filename, $zip);
                } else {
                    $zip->addFile($dir . "/" . $filename);
                    $zip->renameName($dir . "/" . $filename, $filename);
                }
            }
        }
        @closedir($dir);
    }
    public function z_zipdir($dir, $zipfile)
    {
        $zip = new \ZipArchive();
        if ($zip->open($zipfile, \ZipArchive::CREATE) === TRUE) {
            $this->z_addDir2Zip($dir, $zip);
            $zip->close();
        }
    }
    public function cut($begin, $end, $str)
    {
        $b = mb_strpos($str, $begin) + mb_strlen($begin);
        $e = mb_strpos($str, $end) - $b;
        return mb_substr($str, $b, $e);
    }
}
