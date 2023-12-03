<template>
  <div id="app">
    <!-- 路由出口 -->
    <!-- 路由匹配到的组件将渲染在这里 -->
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>

<!-- 设置基础样式 -->
<style lang="less">
html,
body,
h3 {
  margin: 0;
  padding: 0;
}
</style>