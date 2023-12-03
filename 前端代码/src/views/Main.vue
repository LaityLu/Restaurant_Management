<template>
  <div>
    <el-container>
      <el-aside width=auto>
        <common-aside-vue />
      </el-aside>
      <el-container>
        <el-header>
          <common-header />
        </el-header>
        <common-tag />
        <el-main>
          <!-- 路由出口 -->
          <!-- 路由匹配到的组件将渲染在这里 -->
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>


<script>
import CommonAsideVue from '../components/CommonAside.vue';
import CommonHeader from '../components/CommonHeader.vue';
import CommonTag from '../components/CommonTag.vue';

export default {
  data() {
    return {};
  },
  components: {
    CommonAsideVue,
    CommonHeader,
    CommonTag,
  },
};

</script>

<!-- 去除header跟导航菜单栏之间的间距 -->
<style scoped>
.el-header {
  padding: 0;
}
</style>
