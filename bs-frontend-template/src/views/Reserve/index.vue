<template>
  <el-table :data="dataList" stripe style="width: 100%">
    <el-table-column prop="title" label="标题" />
    <el-table-column prop="price_text" label="租金" />
    <el-table-column prop="structure" label="户型" />
    <el-table-column prop="tags" label="配套" />
    <el-table-column prop="area_text" label="面积" />
    <el-table-column prop="city" label="所在城市" />
    <el-table-column prop="location" label="位置" />
    <el-table-column prop="floor" label="楼层" />
  </el-table>
</template>

<script lang="ts" setup>
//rental/reserve
import { onMounted, ref } from "vue";
import { useLayoutStore } from "/@/store/modules/layout";
import { ElNotification } from "element-plus";
const tableData = JSON.parse(localStorage.getItem("reverseData"));
const dataList = ref([]);
onMounted(async () => {
  const { getReserve } = useLayoutStore();

  const res = await getReserve();
  dataList.value = res.data;
  console.log(dataList);
});
</script>
