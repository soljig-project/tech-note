<template>
  <section>
    <h1>Vue.js에서 kakao map api 사용하기</h1>
    <hr>
    <h3>(1) 현재 위치 좌표 값을 이용하여 마커로 표시하기</h3>
    <MapUsingPoints />
    <br>
    <h3>(2) 키워드 검색 결과 지도 위에 마커로 표시하기</h3>
    <MapUsingSearch />
  </section>
</template>

<script>
import MapUsingPoints from '@/components/MapUsingPoints.vue';
import MapUsingSearch from '@/components/MapUsingSearch.vue';

export default {
  name: 'App',
  components: {
    MapUsingPoints,
    MapUsingSearch,
  }
}
</script>

<style scoped>
section {
  width: 90%;
  min-width: 800px;
  margin: 0 auto;
}

h1 {
  font-size: 30px;
  color: crimson;
  text-align: center;
}
</style>