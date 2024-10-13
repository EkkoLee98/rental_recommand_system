<template>
  <Page>
    <div class="bg-white rounded p-4">
      <el-input
        class="w-1/2"
        v-model="form.title__icontains"
        clearable
        placeholder="请输入标题关键词"
        @keyup.enter="search"
      >
        <template #append>
          <el-button type="primary" @click="search">搜索</el-button>
        </template>
      </el-input>
      <el-form class="mt-4" :inline="true">
        <el-form-item label="标签">
          <el-input
            clearable
            v-model="form.tags__icontains"
            placeholder="输入房源标签关键词"
            @change="search"
          ></el-input>
        </el-form-item>
      </el-form>
      <div class="mt-4">
        <span class="text-gray-400 mr-4 text-sm">排序</span>
        <el-radio-group
          @change="search"
          v-model="form.orderby"
          size="small"
          style="display: inline"
        >
          <el-radio label="-id">默认</el-radio>
          <el-radio label="price">价格</el-radio>
        </el-radio-group>
      </div>
    </div>
    <div class="flex flex-col gap-4 mt-10">
      <div
        v-for="i in list"
        :key="i.id"
        class="bg-white rounded p-4 produce flex gap-4"
        @click="toDetail(i.id)"
      >
        <div style="width: 240px; height: 183px">
          <img
            class="rounded"
            :src="i.cover"
            style="
              user-select: none;
              -webkit-user-drag: none;
              width: 100%;
              height: 100%;
            "
            referrerPolicy="no-referrer"
          />
        </div>
        <div>
          <div class="truncate mt-2 text-gray-800 text-lg font-bold">
            {{ i.title }}
          </div>
          <div class="truncate mt-3 text-gray-400 text-sm">
            {{ i.province }}-{{ i.city }}
          </div>
          <div class="truncate mt-3 text-gray-400 text-sm">
            <span>{{ i.location }}</span>
            <span class="mx-2 text-gray-200">/</span>
            <span>{{ i.area_text }}</span>
            <span class="mx-2 text-gray-200">/</span>
            <span>{{ i.orientation }}</span>
            <span class="mx-2 text-gray-200">/</span>
            <span>{{ i.structure }}</span>
          </div>
          <div class="mt-3" v-if="i.tags">
            <el-tag
              v-for="t in i.tags.split(',')"
              :key="t"
              class="mr-2"
              type="info"
              >{{ t }}</el-tag
            >
          </div>
        </div>
        <div class="text-blue-400 ml-4 mt-2 font-bold text-lg">
          {{ i.price_text }}
        </div>
      </div>
    </div>
    <div class="mt-10 flex justify-center">
      <el-pagination
        @current-change="handleCurrentChange"
        :current-page="form.page"
        :page-size="form.pagesize"
        layout="prev, pager, next, jumper, total"
        :total="form.total"
        background
      >
      </el-pagination>
    </div>
    <!-- <Setting /> -->
  </Page>
</template>

<script>
import request from "/@/utils/request";
import Page from "/@/components/Page/index.vue";
// import Setting from "/@/layout/components/sideSetting.vue";
export default {
  components: { Page },
  data() {
    return {
      list: [],
      provinces: [],
      cities: [],
      form: {
        orderby: "-id",
        title__icontains: null,
        total: 0,
        page: 1,
        pagesize: 10,
      },
    };
  },
  beforeMount() {
    this.search();
    request.get("/unique_fields/?field=province").then((res) => {
      this.provinces = res.data;
    });
    request.get("/unique_fields/?field=city").then((res) => {
      this.cities = res.data;
    });
  },
  methods: {
    toDetail(id) {
      this.$router.push({ name: "Detail", params: { id } });
    },
    setCate(idx) {
      let obj = {
        cateName: null,
        cate1Name: null,
        cate2Name: null,
        cate3Name: null,
      };
      this.breadcrumb.slice(0, idx + 1).forEach((v, i) => {
        obj[`cate${i + 1}Name`] = v;
      });
      Object.assign(this.form, obj);
      this.search();
    },
    resetCate() {
      Object.assign(this.form, {
        cateName: null,
        cate1Name: null,
        cate2Name: null,
        cate3Name: null,
      });
      this.search();
    },
    handleCurrentChange(page) {
      this.form.page = page;
      this.getlist();
    },
    search() {
      this.form.page = 1;
      this.getlist();
    },
    getlist() {
      request.post("/rental/", this.form).then((res) => {
        this.list = res.data.result.map((v) => {
          v.cover = v.imgs.split("\n")[0].replace("https", "http");
          return v;
        });
        this.form.total = res.data.total;
      });
    },
  },
};
</script>

<style lang="postcss" scoped>
.produce {
  cursor: pointer;
  transition: all 0.3s;
}
.produce:hover {
  box-shadow: 0 16px 40px 0 hsl(0deg 0% 60% / 30%);
  z-index: 3;
  transform: translateY(-10px);
}
</style>