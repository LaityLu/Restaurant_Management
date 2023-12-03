<template>
  <el-row>
    <el-col :span="8" style="padding-inline: 20px">
      <el-card class="box-card" style="height: 225px">
        <div class="user">
          <img :src="updateImageSource" alt="个人头像" />
          <div class="userinfo">
            <p class="name">{{ username }}</p>
            <p class="access">{{ radio === '0' ? '店长' : (radio === '1' ? '副店长' : '管理员') }}</p>
          </div>
        </div>
        <div class="login-info">
          <!-- <p>上次登录时间：<span>2023-10-1</span></p>
          <p>上次登录地点：<span>郑州</span></p> -->
        </div>
      </el-card>
      <el-card style="margin-top: 20px; height: 330px">
        <el-table :data="tableData" style="width: 100%" :default-sort="{ prop: 'sales', order: 'descending' }">
          <el-table-column prop="M_id__M_name" label="热销菜品" width="190">
          </el-table-column>
          <el-table-column prop="total_quantity" label="总销量/份">
          </el-table-column>
        </el-table>
      </el-card>
    </el-col>
    <el-col :span="15" style="padding-left: 10px">
      <div class="num">
        <el-card v-for="item in countData" :key="item.name" :body-style="{ display: 'flex', padding: 0 }">
          <i class="icon" :class="`el-icon-${item.icon}`" :style="{ background: item.color }"></i>
          <div class="detail">
            <p class="price">{{ item.str }}{{ item.value }}</p>
            <p class="desc">{{ item.name }}</p>
          </div>
        </el-card>
      </div>
      <el-card style="height: 374px">
        <!-- 折线图 -->
        <div ref="echarts1" style="height: 370px"></div>
      </el-card>
    </el-col>
  </el-row>
</template>


<script>
import { getHomeData } from '@/api';
import *as echarts from 'echarts'
import { computed } from 'vue';
import Cookie from 'js-cookie'
import img1 from '../assets/images/1.jpg'
import img2 from '../assets/images/2.jpg'
import img3 from '../assets/images/3.jpg'

export default {
  data() {
    return {
      tableData: [],//菜品销量数据
      countData: [
        {
          name: "今日支付订单数",
          str: "#",
          value: 0,
          icon: "success",
          color: "#2ec7c9",
        },
        {
          name: "本月支付订单数",
          str: "#",
          value: 0,
          icon: "success",
          color: "#2ec7c9",
        },
        {
          name: "今日总收入",
          str: "￥",
          value: 0,
          icon: "s-goods",
          color: "#5ab1ef",
        },
        {
          name: "本月总收入",
          str: "￥",
          value: 0,
          icon: "s-goods",
          color: "#5ab1ef",
        },
      ],//订单卡片数据
      echartsData: [],//折线图数据
      radio: '',
    };
  },
  methods: {
    //获取首页数据
    getHomeinfo() {
      let that = this//axios执行异步请求后,会让 this指向undefine
      getHomeData().then(function (res) {
        //请求成功
        if (res.data.code === 1) {
          for (let i = 0; i < 5; i++) {
            //菜品销量数据
            that.tableData.push(res.data.dish_data[i])
            // console.log(res.data.data)
          }
          //订单卡片数据
          that.countData[0].value = res.data.order_data[0]['today_order_count']
          that.countData[2].value = res.data.order_data[0]['today_total_income']
          that.countData[1].value = res.data.order_data[0]['month_paid_data']
          that.countData[3].value = res.data.order_data[0]['month_total_income']
          //折线图数据
          that.echartsData = res.data.echarts_data
          // console.log(that.echartsData)
          that.getechartsinfo(that.echartsData)
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
    //获取折线图数据
    getechartsinfo(echartsData) {
      // console.log(echartsData)
      // 基于准备好的dom，初始化echarts实例
      const echarts1 = echarts.init(this.$refs.echarts1);
      // 指定图表的配置项和数据
      var echarts1Option = {};
      // 处理数据xAxis
      const xAxis = echartsData.map(item => item.day);
      const xAxisData = {
        data: xAxis,
      };
      const legendData = {
        data: ['完成订单数', '总收入']
      }
      // 提取订单数和总收入数据
      const orderCounts = echartsData.map(item => item.order_count);
      const totalIncomes = echartsData.map(item => item.total_income);
      echarts1Option.xAxis = xAxisData;
      echarts1Option.yAxis = {};
      echarts1Option.legend = legendData;
      echarts1Option.series = [];
      echarts1Option.series.push({
        name: '完成订单数',
        data: orderCounts,
        type: "line",
      });
      echarts1Option.series.push({
        name: '总收入',
        data: totalIncomes,
        type: "line",
      });

      // 使用刚指定的配置项和数据显示图表。
      echarts1.setOption(echarts1Option);
    }
  },
  mounted() {
    this.getHomeinfo()
  },
  computed: {
    updateImageSource() {
      this.username = Cookie.get('username')
      this.radio = Cookie.get('radio')
      if (this.radio === '1') {
        return img1;//副店长
      } else if (this.radio === '0') {
        return img2;//店长
      } else if (this.radio === '2') {
        return img3;//管理员
      }
    }
  }
};
</script>

<style lang="less" scoped>
.user {
  padding-bottom: 10px;
  margin-bottom: 2px;
  border-bottom: 1px solid #ccc;
  display: flex;
  align-items: center;

  img {
    margin-right: 40px;
    width: 130px;
    height: 130px;
    border-radius: 50%;
  }

  .userinfo {
    .name {
      font-size: 30px;
      margin-bottom: 5px;
    }

    .access {
      color: #999999;
    }
  }
}

.login-info {
  p {
    line-height: 14px;
    font-size: 14px;
    color: #999999;

    span {
      color: #666666;
      margin-left: 60px;
    }
  }
}

.num {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;

  .icon {
    width: 80px;
    height: 80px;
    font-size: 30px;
    text-align: center;
    line-height: 80px;
    color: #fff;
  }

  .detail {
    margin-left: 15px;
    display: flex;
    flex-direction: column;
    justify-content: center;

    .price {
      font-size: 20px;
      margin-bottom: 10px;
      line-height: 15px;
      height: 2px;
    }

    .desc {
      font-size: 14px;
      color: #999;
      text-align: center;
    }
  }

  .el-card {
    width: 46%;
    margin-bottom: 20px;
  }
}
</style>
