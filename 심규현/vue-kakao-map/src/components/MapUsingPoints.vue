<template>
  <article>
    <button @click="initMap">현재 나의 위치로 이동</button>
    <div id="map" />
    <p class="my-position"></p>
  </article>
</template>

<script>
export default {
  data() {
    return {
      initLatitude: 33.450701, // 기본 위도 값(제주도 Kakao)
      initLongitude: 126.570667, // 기본 경도 값(제주도 Kakao)
    }
  },
  created() {
    this.getLocation();
  },
  mounted() {
    window.kakao && window.kakao.maps ? this.initMap() : this.addScript();
  },
  updated() {
    this.getLocation();
  },
  methods: {
    getLocation() {
      if (navigator.geolocation) { // GPS 기능을 지원하는 경우에 현재 위치의 위도, 경도 추출
        navigator.geolocation.getCurrentPosition(position => {
          this.initLatitude = position.coords.latitude;
          this.initLongitude = position.coords.longitude;
        }, error => {
          console.error(error);
        }, {
          enableHighAccuracy: false,
          maximumAge: 0,
          timeout: Infinity
        });
      } else { // GPS 기능을 지원하지 않는 경우 지원하지 않는다는 alert 창 띄우기
        alert('GPS를 지원하지 않습니다');
      }
    },
    initMap() {
      let container = document.getElementById('map');
      let options = {
        center: new kakao.maps.LatLng(this.initLatitude, this.initLongitude),
        level: 3
      };
      let map = new kakao.maps.Map(container, options);
      let marker = new kakao.maps.Marker({ position: map.getCenter() }); marker.setMap(map);
      const positionMessage = document.querySelector('.my-position');
      positionMessage.innerText = `현재 나의 위치는 위도: ${this.initLatitude}, 경도: ${this.initLongitude} 입니다.`;
    },
    addScript() {
      const script = document.createElement('script');
      /* global kakao */
      script.onload = () => kakao.maps.load(this.initMap);
      script.src = `http://dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${process.env.VUE_APP_KAKAO_MAP_API_KEY}`;
      document.head.appendChild(script);
    }
  }
} 
</script>

<style scoped>
#map {
  width: 100%;
  height: 400px;
}

button {
  font-weight: 600;
  background: #ddd;
  padding: 4px 8px;
  margin-bottom: 10px;
  border: transparent;
  border-radius: 10px;
  transition: all .2s;
}

button:hover {
  cursor: pointer;
  box-shadow: 2px 4px 4px rgba(0, 0, 0, .1);
}

button:focus {
  outline: none;
}
</style>