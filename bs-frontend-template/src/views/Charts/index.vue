<template>
  <div class="flex justify-center">
    <div class="grid grid-cols-3 w-full mt-10">
      <vue-echarts api="/orientation_map/" class="col-span-2"></vue-echarts>
      <vue-echarts api="/province_map/"></vue-echarts>
      <vue-echarts api="/type_pie/"></vue-echarts>
      <vue-echarts api="/level_bar/"></vue-echarts>
      <vue-echarts api="/price_bar/"></vue-echarts>
    </div>
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