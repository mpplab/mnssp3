<?php

namespace app\index\controller;

use think\Controller;
use think\Db;

class Pql extends Controller
{
    /**
     * PQL查询
     * 
    */
    public function query()
    {
        if (!isset($_POST['sql'])) {
            $data = array('code' => 0, 'msg' => 'fail', 'data' => 'The system is busy, please try again later');
            echo json_encode($data);
            return;
        }
        $sql = $_POST['sql'];
        if (!$sql) {
            $data = array('code' => 0, 'msg' => 'fail', 'data' => 'The system is busy, please try again later');
            echo json_encode($data);
            return;
        }
        $res_sql = $this->SqlToMql($sql);
        if($res_sql['code']==0){
            echo json_encode($res_sql);
            return;
        }else{
            $res_sql = $res_sql['data'];
        }
        try {
            $res = Db::query($res_sql['res_sql']);
        } catch (\Throwable $th) {
            $data = array('code' => 0, 'msg' => 'fail', 'data' => $th->getMessage());
            echo json_encode($data);
            return;
        }
        $res = $res[0][sprintf('%s(%s)', $res_sql['fun'], $res_sql['column'])];
        $res_sql['res'] = $res;
        
        $f = $this->getF($res_sql['table'],$res_sql['column'],$res_sql['fun'],$res_sql['global'],$res_sql['where']);
        if($f['code']>0){
            $f = $f['data'];
            $res_sql['f'] = $f;
        }
        
        $noise_res='';
        /**===========Noise============ */
        $noise_res = $this->Noise($res,$f,$res_sql['with']);
        if($noise_res['code']>0){
            $noise_res = $this->setFloatLength($res,$noise_res['data']); 
            $res_sql['noise_res']= $noise_res;
        }else{
            echo json_encode($noise_res);
            return;
        }
        /**============================ */
        $res=array(
            'noise_res'=>$res_sql['noise_res'],
            'fun'=>$res_sql['fun_user'].'['.$res_sql['column'].']'
    
        );
        $data = array('code' => 1, 'msg' => 'success', 'data' => $res);
        echo json_encode($data);
        return;
    }

    

    /**
     * 解析mql
     * 
    */
    function SqlToMql($sql = null)
    {
        ##################字符组解析Start#########################
        //去前后空格
        $sql = trim($sql);
        //多空格替换
        $sql = preg_replace("/\s(?=\s)/", "\\1", $sql);
        //以where分割
        $sql_where_arr = preg_split("/where/i", $sql);
        if(count($sql_where_arr)>1){
            $sql_where_arr[1] = trim($sql_where_arr[1]);
        }
        $res_sql = '';
        $select = '';
        $from = '';
        $where = '';
        $with = '';
        $global ='';
        $table='';
        //以空格分割
        $sql_arr = explode(' ', trim($sql_where_arr[0]));
        //protect->from
        if (strcasecmp($sql_arr[0], 'protect') == 0) {
            $from = ' from '.$sql_arr[1];
            $table = $sql_arr[1];
        } else {
            return $data = array('code' => 0, 'msg' => 'fail', 'data' => 'Not a correct keyword:'.$sql_arr[0]);
        }
        
        //pick->select
        if (strcasecmp($sql_arr[2], 'pick') == 0) {
            if(!$this->checkStr($sql_arr[3],'[]')){
                return $data = array('code' => 0, 'msg' => 'fail', 'data' => 'Function format error:'.$sql_arr[3]);
            }
            $column = [];
            $preg = '/(?<=\[)[^\]]+/';
            preg_match_all($preg,$sql_arr[3],$column);
            if($column[0]){
                $column =  $column[0][0];
            }else{
                return $data = array('code' => 0, 'msg' => 'fail', 'data' => 'Function parameter error:'.$sql_arr[3]);
            }
            $fun = preg_replace('/\[.*?\]/', '', $sql_arr[3]);
            $fun_user = strtoupper($fun);
            switch ($fun) {
                case strcasecmp($fun, 'avg') == 0:
                    $fun = 'avg';
                    break;
                case strcasecmp($fun, 'total') == 0:
                    $fun = 'sum';
                    break;
                case strcasecmp($fun, 'highest') == 0:
                    $fun = 'max';
                    break;
                case strcasecmp($fun, 'lowest') == 0:
                    $fun = 'min';
                    break;  
                case strcasecmp($fun, 'count') == 0:
                    $fun = 'count';
                    if($column!='*'){
                        return $data = array('code' => 0, 'msg' => 'fail', 'data' => 'The [] in the Compute function must be *:');
                    }
                    break;          
                default:
                    return $data = array('code' => 0, 'msg' => 'fail', 'data' => 'Not a correct function:'.$fun);
            }
            $select = sprintf('select %s(%s)', $fun, $column);
        } else {
            return $data = array('code' => 0, 'msg' => 'fail', 'data' => 'Not a correct keyword:'.$sql_arr[2]);
        }
        //with
        if (strcasecmp($sql_arr[4], 'with') == 0) {
            if(count($sql_arr)>6){
                for ($i=6; $i < count($sql_arr); $i++) { 
                    if(strcasecmp($sql_arr[$i], 'global') != 0){
                        $sql_arr[5] .= $sql_arr[$i];
                    }
                }
            }
            $with =$sql_arr[5]; 
            if(!is_numeric($with)){
                return $data = array('code' => 0, 'msg' => 'fail', 'data' => 'The keyword With must be a number');
            }
            
        }else if(strcasecmp(preg_replace('/\(.*?\)/', '', $sql_arr[4]), 'withrange') == 0){
            //withrange
            $preg = '/(?<=\()[^\)]+/';
            preg_match_all($preg,$sql_arr[4],$rang);
            if($rang[0]){
                $rang =  $rang[0][0];
            }else{
                return $data = array('code' => 0, 'msg' => 'fail', 'data' => 'WITHRANGE parameter error');
            }
            $rang = explode(',',$rang);
            if(count($rang)==2){
                if($rang[1]>=$rang[0]){
                    $with = $this->mt_rand_float($rang[0],$rang[1]);
                }else{
                    return $data = array('code' => 0, 'msg' => 'fail', 'data' => 'WITHRANGE parameter error');
                }
            }else{
                return $data = array('code' => 0, 'msg' => 'fail', 'data' => 'WITHRANGE parameter error');
            }
            if(count($sql_arr)>5 && strcasecmp($sql_arr[4+1], 'global') != 0){
                return $data = array('code' => 0, 'msg' => 'fail', 'data' => $sql_arr[4+1].' is not a correct keyword');
            }
           
        }else {
            return $data = array('code' => 0, 'msg' => 'fail', 'data' => 'Not a correct keyword:'.$sql_arr[4]);
        }
        //global
        for ($i=0; $i < count($sql_arr); $i++) { 
            if(strcasecmp($sql_arr[$i], 'global') == 0 ){
                if($i==count($sql_arr)-1){
                    $global = 'global';
                }else{
                    return $data = array('code' => 0, 'msg' => 'fail', 'data' => $sql_arr[$i+1].' is not a correct keyword');
                }
            }
        }

        $sql = "select count(table_name) from information_schema.tables where table_schema='lunwen' and table_name = '{$table}';";
        $count = Db::query($sql);
        $count = $count[0]['count(table_name)'];
        if($count == 0){
            return $data = array('code' => 0, 'msg' => 'fail', 'data' => "Table '{$table}' doesn't exist"); 
        }
        if($fun!='count'){
            $sql = "select count(COLUMN_NAME) from information_schema.COLUMNS where table_name = '{$table}' AND COLUMN_NAME = '{$column}';";
            $count = Db::query($sql);
            $count = $count[0]['count(COLUMN_NAME)'];
            if($count == 0){
                return $data = array('code' => 0, 'msg' => 'fail', 'data' => "Unknown column '{$column}' in 'field list'"); 
            }
        }
        if (count($sql_where_arr) == 1) {
            //不带where
            $res_sql = $select.$from;
        } else if (count($sql_where_arr) > 1) {
            //带where
            $where = sprintf(' where %s',$sql_where_arr[1]);
            $res_sql = $select.$from.$where;
        }
        if(count($sql_where_arr)>1){
            $where = $sql_where_arr[1];
        }
        $res_data = array(
            'res_sql'=>$res_sql
            ,'table'=>$table
            ,'column'=>$column
            ,'fun'=>$fun
            ,'with'=>$with
            ,'global'=>$global
            ,'where'=>$where
            ,'fun_user'=>$fun_user
        );
        
        return $data = array('code' => 1, 'msg' => 'success', 'data' => $res_data);
        ##################字符组解析End#########################
    }

    /**
     * 判断一个字符串中的括号是否闭合
     * @access private
     * @param string $str 判断字符串
     * @param string $mark 判断符号
     * @return bool 
    */
    function checkStr($str,$mark) 
    {
        if(empty($str)) {
            return false;
        }
        if(empty($mark)||strlen($mark)!=2){
            return false;
        }
        if(strpos($str, $mark[0] ) ===false && strpos($str, $mark[1] ) ===false) {
            return false;
        }
        $str_len = strlen($str);
        $j = $z = 0;
        for ($i=0; $i < $str_len; $i++) { 
            if($str[$i] == $mark[0]) {
                $j++;
            }
            if($str[$i] == $mark[1]) {
                if($j > 0) {
                    $j--;
                }else{
                    $z = 1;
                }
            }
        }
        if(empty($j) && empty($z)) {
            return true;
        }
        return false;
    }
    /**
     * 统一小数点位数
     */
    function setFloatLength($num,$res_num) {
        $count = 0;
        $temp = explode ( '.', $num );
        if (sizeof ( $temp ) > 1) {
            $decimal = end ( $temp );
            $count = strlen ( $decimal );
        }
        return $res_num = round($res_num,$count);
    }

    /**
     * 隐私加噪
     */
    function Noise($num,$z,$e)
    {
        if(empty($num)||empty($e)||empty($z)) {
            return $data = array('code'=>0,'msg'=>'fail','data'=>'参数错误');
        }
        $exec = "python3 Python/dp.py {$num} {$z} {$e} 2>&1";
        $output = exec($exec, $out, $status);
        if ($status > 0) {
            return $data = array('code' => 0, 'msg' => 'fail', 'data' => 'The system is busy, please try again later');
        } else {
            return $data = array('code' => 1, 'msg' => 'success', 'data' => $output); 
        }
    }
    /**
     * 利用mt_rand生成0~1随机小数[更好的随机小数]
     * @param  int   $min
     * @param  int   $max
     * @return float
    */
    function mt_rand_float($min=0, $max=1){
        return $min +  abs($max-$min) * mt_rand(0,mt_getrandmax())/mt_getrandmax();
    
    }

    /**
     * 获取敏感度
     * @param string $table 表名
     * @param string $column 字段名
     * @param string $fun 函数名
     * @param string $global 是否全局 
     * @param string $where 条件 
     * @return float
     */
    function getF($table,$column,$fun,$global=null,$where=null){
        if(empty($table)||empty($column)||empty($fun)) {
            return $data = array('code'=>0,'msg'=>'fail','data'=>'参数错误');
        }
        switch ($fun) {
            case 'avg':
                $where = $where;
                if(!$global&&$where){
                    $where =" where {$where}";
                }else{
                    $where=null;
                }
                //计算真是avg
                $sql = "select avg({$column}) from {$table} {$where}";
                try {
                    $res = Db::query($sql);
                } catch (\Throwable $th) {
                    return $data = array('code' => 0, 'msg' => 'fail', 'data' => $th->getMessage());
                }
                $res = $res[0][sprintf('avg(%s)',$column)];
                $avg1 = $res;
                //获取最大值
                $sql = "select max({$column}) from {$table} {$where}";
                try {
                    $res = Db::query($sql);
                } catch (\Throwable $th) {
                    return $data = array('code' => 0, 'msg' => 'fail', 'data' => $th->getMessage());
                }
                $res = $res[0][sprintf('max(%s)',$column)];
                $max = $res;

                //获取最小值
                $sql = "select min({$column}) from {$table} {$where}";
                try {
                    $res = Db::query($sql);
                } catch (\Throwable $th) {
                    return $data = array('code' => 0, 'msg' => 'fail', 'data' => $th->getMessage());
                }
                $res = $res[0][sprintf('min(%s)',$column)];
                $min = $res;

                //求差值
                $c = abs($avg1-$min)-abs($max-$avg1);
                if($c>0){
                    $c=$min;
                }else{
                    $c=$max;
                }

                //计算删除差值后的平均值
                //求和
                $sql = "select sum({$column}) from {$table} {$where}";
                try {
                    $res = Db::query($sql);
                } catch (\Throwable $th) {
                    return $data = array('code' => 0, 'msg' => 'fail', 'data' => $th->getMessage());
                }
                $sum = $res[0][sprintf('sum(%s)',$column)];
                //减差值
                $sum = $sum - $c;
                //求个数
                $sql = "select count({$column}) from {$table} {$where}";
                try {
                    $res = Db::query($sql);
                } catch (\Throwable $th) {
                    return $data = array('code' => 0, 'msg' => 'fail', 'data' => $th->getMessage());
                }
                $count = $res[0][sprintf('count(%s)',$column)];
                $count = $count-1;
                $avg2 = $sum/$count;
                
                $res = abs($avg2 - $avg1);
                return $data = array('code' => 1, 'msg' => 'success', 'data' => $res); 
                break;
            case 'sum':
                $sql = "select max({$column}) from {$table} ";
                if(!$global&&$where){
                    $sql = $sql." where {$where}";
                }
                try {
                    $res = Db::query($sql);
                } catch (\Throwable $th) {
                    return $data = array('code' => 0, 'msg' => 'fail', 'data' => $th->getMessage());
                }
                $res = $res[0][sprintf('max(%s)',$column)];
                $res = abs($res);
                return $data = array('code' => 1, 'msg' => 'success', 'data' => $res); 
                break;
            case 'max':
                // select  total from expenses  ORDER BY total desc LIMIT 2
                $where = $where;
                if(!$global&&$where){
                    $where =" where {$where}";
                }else{
                    $where=null;
                }
                $sql = "select distinct {$column} from {$table} {$where} ORDER BY {$column} desc LIMIT 2";
                try {
                    $res = Db::query($sql);
                } catch (\Throwable $th) {
                    return $data = array('code' => 0, 'msg' => 'fail', 'data' => $th->getMessage());
                }
                $res = $res[0][$column]-$res[1][$column];
                $res = abs($res);
                return $data = array('code' => 1, 'msg' => 'success', 'data' => $res); 
                break;
            case 'min':
                $where = $where;
                if(!$global&&$where){
                    $where =" where {$where}";
                }else{
                    $where=null;
                }
                $sql = "select distinct {$column} from {$table} {$where} ORDER BY {$column} LIMIT 2";
                try {
                    $res = Db::query($sql);
                } catch (\Throwable $th) {
                    return $data = array('code' => 0, 'msg' => 'fail', 'data' => $th->getMessage());
                }
                $res = $res[0][$column]-$res[1][$column];
                $res = abs($res);
                return $data = array('code' => 1, 'msg' => 'success', 'data' => $res); 
                break;  
            case 'count':
                return $data = array('code' => 1, 'msg' => 'success', 'data' => 1); 
                break;          
            default:
                // echo '函数关键字错误';
                return $data = array('code' => 0, 'msg' => 'fail', 'data' => '函数关键字错误');
        }
    }
}
