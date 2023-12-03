<template>
  <div style="padding-left:60px">
    <!-- 提示窗 -->
    <el-dialog :title="dialogTitle" :before-close="handleClose" :visible.sync="dialogVisible" width="50%"
      :close-on-click-modal="false">
      <!-- 菜品表单信息 -->
      <el-form ref="form" :rules="rules" :inline="true" :model="form" label-width="80px" label-position="right">
        <el-form-item label="编号" prop="M_id">
          <el-input placeholder="请输入编号" v-model="form.M_id" suffix-icon="el-icon-edit" :disabled="isEdit"></el-input>
        </el-form-item>
        <el-form-item label="菜名" prop="M_name">
          <el-input placeholder="请输入菜名" v-model="form.M_name" suffix-icon="el-icon-edit"></el-input>
        </el-form-item>
        <el-form-item label="类别" prop="M_class">
          <el-select v-model="form.M_class" placeholder="请选择类别">
            <el-option label="肉类主菜" value="肉类主菜"></el-option>
            <el-option label="冷盘凉菜" value="冷盘凉菜"></el-option>
            <el-option label="米面主食" value="米面主食"></el-option>
            <el-option label="暖胃煲汤" value="暖胃煲汤"></el-option>
            <el-option label="素菜小炒" value="素菜小炒"></el-option>
            <el-option label="甜品点心" value="甜品点心"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="价格" prop="M_price">
          <el-input placeholder="请输入价格" v-model="form.M_price" suffix-icon="el-icon-edit"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submit">确 定</el-button>
        <el-button type="info" @click="cancel">取 消</el-button>
      </span>
    </el-dialog>
    <div class=functionstyle>
      <!-- 新增按钮 -->
      <el-button @click="addform()" type="primary" icon="el-icon-circle-plus-outline" style="margin-bottom: 14px" plain
        size="medium">新增
      </el-button>
      <el-button @click="handelExportToExcel()" type="primary" icon="el-icon-download" style="margin-bottom: 14px" plain
        size="medium">导出Excel
      </el-button>
      <el-form :inline="true" style="margin-left: 320px ">
        <el-form-item prop="query">
          <el-input v-model="inputstr" placeholder="请输入查询条件" :clearable="true">
          </el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="queryDishData" icon="el-icon-search" plain size="medium">
            查询
          </el-button>
          <el-button type="primary" @click="getALLDishData" icon="el-icon-tickets" plain size="medium">
            全部
          </el-button>
        </el-form-item>
      </el-form>
    </div>
    <div>
      <el-table :data="pagetable" :border="true" stripe style="width: 70%">
        <el-table-column prop="M_id" label="编号" width="180">
        </el-table-column>
        <el-table-column prop="M_name" label="菜名" width="180">
        </el-table-column>
        <el-table-column prop="M_class" label="类别" width="180">
        </el-table-column>
        <el-table-column prop="M_price" label="价格" width="180">
        </el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button type="success" size="mini" icon="el-icon-edit" @click="updateform(scope.row)">
            </el-button>
            <el-button type="danger" size="mini" icon="el-icon-delete" @click="deleteDishData(scope.row)">
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <!-- 分页 -->
    <el-row style="margin-top: 10px;padding-right: 20px;">
      <el-col style="text-align: right;">
        <el-pagination @current-change="handleCurrentChange" :current-page.sync="currentpage" :page-size="pagesize"
          layout="total, prev, pager, next, jumper" :total="total">
        </el-pagination>
      </el-col>
    </el-row>
  </div>
</template>

<style lang="less" scoped>
.functionstyle {
  display: flex;
  // justify-content: space-between;
  align-items: center;
}
</style>

<script>
import { getDish } from '@/api';
import { queryDish } from '@/api'
import { checkDid } from '@/api'
import { addDish } from '@/api'
import { updateDish } from '@/api'
import { deleteDish } from '@/api'
import { exportToExcel } from '@/api'
import Cookie from 'js-cookie';

export default {
  data() {
    //校验菜品编号是否存在
    const rulesM_id = (rules, value, callback) => {
      if (this.isEdit) {
        callback()
      }
      //使用Axios进行校验
      checkDid(value).then(res => {
        //请求成功
        if (res.data.code === 1) {
          if (res.data.exist) {
            callback(new Error("编号已存在！"))
          } else {
            callback()
          }
        } else {
          //请求失败
          callback("后端校验编号出现异常！")
        }
      }).catch((err) => {
        console.log(err)
      })
    }
    return {
      dialogTitle: '',
      dialogVisible: false,
      isEdit: false,//标识是否是修改
      total: 0,//数据总行数
      currentpage: 1,//当前页码
      pagesize: 8,//每页行数
      pagetable: [],//分页后当前页的数据
      form: {
        M_id: '',
        M_name: '',
        M_class: '',
        M_price: '',
      },
      rules: {
        M_id: [
          { required: true, message: "请输入编号", trigger: 'blur', },
          { pattern: /^\d+$/, message: "必须是数字", trigger: 'blur' },
          { validator: rulesM_id, trigger: 'blur' },
        ],
        M_name: [
          { required: true, message: "请输入菜名", trigger: 'blur', },
          { pattern: /^[\u4e00-\u9fa5]{1,10}$/, message: "必须是1~10个汉字", trigger: 'blur' },
        ],
        M_class: [{
          required: true, message: "请选择类别", trigger: 'change',
        }],
        M_price: [
          { required: true, message: "请输入价格", trigger: 'blur', },
          { pattern: /^\d+$/, message: "必须是数字", trigger: 'blur' },
        ],
      },
      tableData: [],//表格数据
      inputstr: '',//接收查询条件
      raido: ''
    };
  },
  methods: {
    //弹出表单
    //"添加菜品"表单
    addform() {
      //修改标题
      this.dialogTitle = "添加新菜品"
      //弹出表单
      this.dialogVisible = true
    },
    //"修改菜品"表单
    updateform(row) {
      //修改标题
      this.dialogTitle = "修改菜品信息"
      //标识修改
      this.isEdit = true
      //深拷贝
      this.form = JSON.parse(JSON.stringify(row))
      this.dialogVisible = true
    },
    //点击确定，提交表单
    submit() {
      this.$refs.form.validate((valid) => {
        //console.log(valid,'valid')
        const formData = { ...this.form };
        if (valid) {
          //校验成功后，执行添加或修改
          if (this.isEdit) {
            //修改
            this.updateDishData()
          }
          else {
            //添加
            this.addDishData(formData)
          }
          this.handleClose()
        } else {
          //校验失败
          console.log("error submit!")
          return false
        }
      })
    },
    //弹窗关闭的时候触发
    handleClose() {
      //清除表单中的信息
      this.form = {}
      //清除表单的校验
      this.$refs.form.resetFields()
      this.dialogVisible = false
      this.isEdit = false
    },
    //点击取消
    cancel() {
      this.handleClose()
    },
    //添加新菜品
    addDishData(formData) {
      let that = this
      addDish(formData).then(res => {
        //执行成功
        if (res.data.code === 1) {
          //获取所有员工信息
          that.tableData = res.data.data
          //获取当前返回记录的总行数
          that.total = res.data.data.length
          //获取当前页的数据
          that.getPageData()
          that.$message({
            message: '添加成功',
            type: 'success'
          })
        }
        else {
          //请求失败
          that.$message.error(res.data.msg)
        }
      }).catch(err => {
        //执行失败
        console.log(err)
        that.$message.error("后端插入数据出现问题！")
      })
    },
    //实现修改功能
    updateDishData() {
      let that = this
      updateDish(that.form).then(res => {
        //执行成功
        if (res.data.code === 1) {
          //获取所有菜品信息
          that.tableData = res.data.data
          //获取当前返回记录的总行数
          that.total = res.data.data.length
          //获取当前页的数据
          that.getPageData()
          that.$message({
            message: '修改成功',
            type: 'success'
          })
        }
        else {
          //请求失败
          that.$message.error(res.data.msg)
        }
      }).catch(err => {
        //执行失败
        console.log(err)
        that.$message.error("后端修改数据出现问题！")
      })
    },
    //实现删除功能
    deleteDishData(row) {
      this.$confirm('是否确认删除该菜品【编号: ' + row.M_id + '\t菜名: ' + row.M_name + '】的信息？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        //确认删除
        let that = this
        deleteDish(row.M_id).then(res => {
          //执行成功
          if (res.data.code === 1) {
            //获取所有菜品信息
            that.tableData = res.data.data
            //获取当前返回记录的总行数
            that.total = res.data.data.length
            //获取当前页的数据
            that.getPageData()
            that.$message({
              message: '删除成功!',
              type: 'success'
            })
          }
          else {
            //请求失败
            that.$message.error(res.data.msg)
          }
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        });
      });
    },
    //获取菜品信息
    getDishData: function () {
      let that = this//axios执行异步请求后,会让 this指向undefine
      getDish().then(function (res) {
        //请求成功
        if (res.data.code === 1) {
          that.tableData = res.data.data
          //获取当前返回记录的总行数
          that.total = res.data.data.length
          //获取当前页的数据
          that.getPageData()
          // console.log(that.pagetable)
          //提示
          // that.$message({
          //   message: '数据加载成功',
          //   type: 'success'
          // })
        }
        else {
          //请求失败
          that.$message.error(res.data.msg)
        }
      }).catch(function (err) {
        console.log(err)
        that.$message.error("获取后端数据出现问题！")
      })
    },
    //获取当前页数据
    getPageData() {
      //清空pagetable的数据
      this.pagetable = []
      //获取当前页的数据
      for (let i = (this.currentpage - 1) * this.pagesize; i < this.total; i++) {
        //遍历数据添加到pagetable
        this.pagetable.push(this.tableData[i])
        //判断是否达到一页的要求
        if (this.pagetable.length === this.pagesize) break
      }
    },
    //修改当前的页码
    handleCurrentChange(pageNum) {
      //修改页码
      this.currentpage = pageNum
      //重新分页
      this.getPageData()
    },
    //实现"全部"按钮功能
    getALLDishData() {
      //清空查询条件
      this.inputstr = ''
      //获取全部数据
      this.getDishData()
    },
    //查询菜品信息
    queryDishData() {
      if (this.inputstr === '') {
        this.$message({
          message: '查询条件不能为空！',
          type: 'warning'
        });
        return
      }
      //使用Ajax请求---post---传递inputstr
      let that = this
      queryDish(that.inputstr).then(function (res) {
        //请求成功
        if (res.data.code === 1) {
          that.tableData = res.data.data
          //获取当前返回记录的总行数
          that.total = res.data.data.length
          //获取当前页的数据
          that.getPageData()
          //提示
          that.$message({
            message: '查询成功',
            type: 'success'
          })
        }
        else {
          //查询失败
          that.$message.error(res.data.msg)
        }
      }).catch(function (err) {
        console.log(err)
        that.$message.error("获取后端查询结果出现问题！")
      })
    },
    //导出到Excel
    handelExportToExcel() {
      let that = this
      exportToExcel("Menu").then(res => {
        //执行成功
        if (res.data.code === 1) {
          let url = 'http://127.0.0.1:8000/' + 'media/' + res.data.name;
          // console.log(url)
          window.open(url)
          that.$message({
            message: '下载成功',
            type: 'success'
          })
        }
        else {
          //请求失败
          that.$message.error("导出到Excel出现异常!")
        }
      }).catch(err => {
        //执行失败
        console.log(err)
      })
    },
  },
  mounted() {
    this.getDishData();
  },
  computed: {
    //控制按钮是否禁用
    isButtonDisabled() {
      this.radio = Cookie.get('radio')
      return this.radio === '0' ? false : true;
    },
  }
};
</script>
