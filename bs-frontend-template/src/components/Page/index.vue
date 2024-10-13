<template>
  <div>
    <div class="container">
      <div class="left">
        <slot />
      </div>
      <div class="right">
        <slot name="right">
          <div class="font-bold text-black-400 mb-5 text-lg text-center">
            算法推荐
          </div>
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

          <div class="font-bold text-black-400 mb-5 mt-20 text-lg text-center">
            系统公告
          </div>
          <div class="flex flex-col items-center gap-4">
            <div
              v-for="i in notifyList"
              :key="i.id"
              class="bg-white rounded p-4 produce w-full"
            >
              <div class="truncate mt-2 text-gray-800 text-sm">
                {{ i.title }}
              </div>
              <div class="truncate mt-2 text-gray-400 text-sm">
                {{ i.content }}
              </div>
              <div class="text-red-600 mt-3">{{ i.createTime }}</div>
            </div>
            <el-empty
              :image-size="200"
              v-if="list.length == 0"
              description="暂无相关产品"
            />
          </div>
        </slot>
      </div>
    </div>
  </div>
</template>

<script>
import request from "/@/utils/request";
export default {
  data() {
    return {
      list: [],
      notifyList: [],
    };
  },
  async created() {
    const { data } = await request.get("/rental/recommmand/");
    this.list = data.map((v) => {
      v.cover = v.imgs.split("\n")[0].replace("https", "http");
      return v;
    });

    const { data: notifyList } = await request.get("rental/notify/get/");
    this.notifyList = notifyList.list;
  },
  methods: {
    toDetail(id) {
      this.$router.push({ name: "Detail", params: { id } });
    },
  },
};
</script>

<style lang="postcss" scoped>
.container {
  margin: 20px auto;
  max-width: 70%;
  display: grid;
  grid-template-columns: 80% 20%;
  column-gap: 30px;
}
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