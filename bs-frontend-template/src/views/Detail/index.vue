<template>
  <Page v-loading="loading">
    <div v-if="detail">
      <h1 class="text-2xl text-gray-800 font-bold mb-5">{{ detail.title }}</h1>
      <div class="flex gap-4">
        <el-image
          style="width: 565px; height: 319px"
          :src="detail.cover"
          referrerPolicy="no-referrer"
        ></el-image>
        <el-descriptions column="1" size="large" class="border p-4 w-full">
          <el-descriptions-item label="所属城市:">
            <span class="text-gray-800"
              >{{ detail.province }}-{{ detail.city }}</span
            >
          </el-descriptions-item>
          <el-descriptions-item label="房源位置:">
            <span class="text-gray-800">{{ detail.location }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="租赁方式:">
            <span class="text-gray-800">{{ detail.type }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="房屋类型:">
            <span class="text-gray-800"
              >{{ detail.structure }} {{ detail.area_text }}</span
            >
          </el-descriptions-item>
          <el-descriptions-item label="朝向楼层:">
            <span class="text-gray-800"
              >{{ detail.orientation }} {{ detail.level }}/{{
                detail.floor
              }}层</span
            >
          </el-descriptions-item>
          <el-descriptions-item label="标签:">
            <span v-if="detail.tags">
              <el-tag
                v-for="t in detail.tags.split(',')"
                :key="t"
                class="mr-2"
                type="info"
                >{{ t }}</el-tag
              >
            </span>
          </el-descriptions-item>
          <el-descriptions-item label="价格:">
            <span class="text-blue-400 text-lg font-bold">{{
              detail.price_text
            }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="预定:">
            <el-button type="primary" @click="reserve()">预定</el-button>
          </el-descriptions-item>
        </el-descriptions>
      </div>
      <div v-html="detail.detail" class="content"></div>
      <div class="mt-10">
        <div v-for="i in detail.imgs.split('\n')" :key="i">
          <img
            class="rounded"
            :src="i"
            referrerPolicy="no-referrer"
            v-if="
              i !=
              'https://s1.ljcdn.com/matrix_pc/dist/pc/src/resource/default/565-319.png?_v=20220908152455b3e'
            "
          />
        </div>
      </div>
    </div>
    <template #right>
      <div class="font-bold text-black-400 mb-5 text-center">相关推荐</div>
      <div class="flex flex-col items-center gap-4">
        <div
          v-for="i in list"
          :key="i.id"
          class="bg-white rounded p-4 produce w-full"
          @click="toDetail(i.id)"
        >
          <div style="width: 170px; height: 127px" class="m-auto">
            <img
              class="rounded"
              :src="i.cover"
              referrerPolicy="no-referrer"
              style="
                user-select: none;
                -webkit-user-drag: none;
                width: 100%;
                height: 100%;
              "
            />
          </div>
          <div class="truncate mt-2 text-gray-800 text-sm">
            {{ i.title }}
          </div>
          <div class="truncate mt-2 text-gray-400 text-sm">
            {{ i.location }}
          </div>
          <div class="text-red-600 mt-3">{{ i.price_text }}</div>
        </div>
        <el-empty
          :image-size="200"
          v-if="list.length == 0"
          description="暂无相关产品"
        />
      </div>
    </template>
  </Page>
</template>

<script>
import request from "/@/utils/request";
import Page from "/@/components/Page/index.vue";
import { ElNotification } from "element-plus";
export default {
  components: { Page },
  props: ["id"],
  async created() {
    this.loading = true;
    const { data } = await request.post("/rental/detail/", { id: this.id });
    data.cover = data.imgs.split("\n")[0].replace("https", "http");
    this.detail = data;
    const {
      data: { result },
    } = await request.post("/rental/", {
      location__icontains: this.detail.location
        .split("-")
        .slice(0, 2)
        .join("-"),
      page: 1,
      pagesize: 5,
      orderby: "?",
    });
    this.list = result.map((v) => {
      v.cover = v.imgs.split("\n")[0].replace("https", "http");
      return v;
    });
    this.loading = false;
  },
  data() {
    return {
      number: 0,
      list: [],
      loading: false,
      detail: null,
    };
  },
  methods: {
    async reserve() {
      // 'rental/reserve'
      const { data } = await request.post("rental/reserve/", {
        title: this.detail.title,
        price_text: this.detail.price_text,
        structure: this.detail.structure,
        tags: this.detail.tags,
        area_text: this.detail.area_text,
        city: this.detail.city,
        location: this.detail.location,
        floor: this.detail.floor,
      });

      const { success, message } = data;
      if (success) {
        ElNotification({
          title: "提示",
          message: message,
          type: "success",
        });
      } else {
        ElNotification({
          title: "提示",
          message: message,
          type: "error",
        });
      }
      // const tmpArr =
      //   localStorage.getItem("reverseData") == null
      //     ? []
      //     : JSON.parse(localStorage.getItem("reverseData"));
      // console.log(tmpArr);
      // tmpArr.push(this.detail);
      // localStorage.setItem("reverseData", JSON.stringify(tmpArr));
    },
    toDetail(id) {
      this.$router.push({ name: "Detail", params: { id } });
    },
    jsonify(text) {
      return JSON.parse(text);
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

<style>
.el-descriptions__body {
  background-color: transparent !important;
}

.content h3 {
  font-size: 24px;
  font-weight: 700;
}
.content__article__info h3 {
  padding-top: 60px;
  margin-bottom: 30px;
  line-height: 33px;
  font-size: 24px;
  color: #101d37;
}

.content__article__info ul li:nth-of-type(3n + 1) {
  width: 23.33%;
  font-size: 18px;
  color: rgba(16, 29, 55, 0.6);
}
.content__article__info ul li {
  width: 33%;
  text-align: left;
  line-height: 18px;
  font-size: 16px;
  margin-bottom: 18px;
}
.oneline {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}
.fl {
  float: left;
}
.content__article__info2 {
  overflow: hidden;
  padding-left: 140px;
  position: relative;
  margin-bottom: 7px;
}
.content__article__info2 li:first-of-type {
  font-size: 18px;
  width: 27.08%;
  position: absolute;
  left: 0;
  top: 0;
  text-align: left;
  color: rgba(16, 29, 55, 0.6);
}
.content__article__info2 li {
  width: 20%;
  text-align: center;
  margin-bottom: 28px;
}
.content__article__info2 li.facility_no {
  color: #969696;
  text-decoration: line-through;
}
#info {
  overflow: hidden;
}
.cost_content {
  width: 100%;
  padding-left: 0;
}
.cost_content .price_title {
  display: flex;
  justify-content: space-between;
  line-height: 22px;
  margin-bottom: 10px;
}
.cost_content .table_wrapper .table_title {
  display: flex;
  line-height: 22px;
  justify-content: space-between;
  margin-bottom: 16px;
}
.cost_content .table_wrapper .table_content .table_row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  line-height: 22px;
  font-family: HiraginoSansGB-W3;
  font-size: 16px;
  color: #101d37;
}
.question_icon {
  display: none;
}
.cost_content .table_wrapper .table_col:first-child {
  text-align: left;
}
.cost_content .table_wrapper .font_gray {
  color: #101d37;
  opacity: 0.6;
}
.cost_content .table_wrapper .table_col {
  box-sizing: border-box;
  flex: 1 1 20%;
  text-align: center;
  font-family: PingFangSC-Regular;
  font-size: 16px;
  color: #101d37;
  letter-spacing: 0;
}
</style>