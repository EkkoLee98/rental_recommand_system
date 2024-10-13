<template>
  <div class="flex justify-center">
    <el-tabs tab-position="left" class="w-2/3 mt-10" v-model="index">
      <el-tab-pane label="租房类型统计" name="1">
        <vue-echarts api="/type_pie/" v-if="index == 1"></vue-echarts>
      </el-tab-pane>
      <el-tab-pane label="房屋朝向分析" name="2">
        <vue-echarts api="/orientation_map/" v-if="index == 2"></vue-echarts>
      </el-tab-pane>
      <el-tab-pane label="楼层类型分析" name="3">
        <vue-echarts api="/level_bar/" v-if="index == 3"></vue-echarts>
      </el-tab-pane>
      <el-tab-pane label="房源数量分布" name="4">
        <vue-echarts api="/province_map/" v-if="index == 4"></vue-echarts>
      </el-tab-pane>
      <el-tab-pane label="房源价格分布" name="5">
        <vue-echarts api="/price_bar/" v-if="index == 5"></vue-echarts>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
export default {
  data() {
    return {
      index: "1",
    };
  },
};
</script>