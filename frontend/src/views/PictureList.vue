<template>
  <div>
    <el-table :data="pictures" border style="width: 100%">
      <el-table-column fixed prop="id" label="编号" width="80">
      </el-table-column>
      <el-table-column prop="name" label="名称" width="180"> </el-table-column>
      <el-table-column prop="md5" label="图片名称"> </el-table-column>
      <el-table-column prop="content_type" label="类型"></el-table-column>
      <el-table-column prop="create_time" label="创建时间"></el-table-column>
      <el-table-column prop="update_time" label="更新时间"></el-table-column>
      <el-table-column fixed="right" label="操作" width="100">
        <template slot-scope="scope" id="#flow-img">
          <el-button @click="handleClick(scope.row)" type="text" size="small"
            >查看</el-button
          >
          <el-button type="text" size="small">编辑</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div id="flow-img"></div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      pictures: []
    };
  },
  created() {
    this.axios
      .get("http://47.95.212.82:8000/files/?page=1")
      .then(response => {
        this.pictures = response.data.items;
      })
      .catch(function(error) {
        // 请求失败处理
        console.log(error);
      });
  },
  mounted() {},
  methods: {
    handleClick(row) {
      this.axios({
        method: "get",
        url: "http://47.95.212.82:8000/downloadfiles/?id=" + row.id,
        responseType: "image/jpeg"
      })
        .then(response => {
          console.log(response);
          var img = document.createElement("img");
          const myBlob = new window.Blob([response], { type: "image/jpeg" });
          const qrUrl = window.URL.createObjectURL(myBlob);
          img.src = qrUrl;
          img.onload = function() {
            window.URL.revokeObjectURL(qrUrl);
          };
          const imgDiv = document.querySelector("#flow-img");
          console.log(imgDiv)
          imgDiv.appendChild(img);
        })
        .catch(function(error) {
          // 请求失败处理
          console.log(error);
        });
    }
  }
};
</script>