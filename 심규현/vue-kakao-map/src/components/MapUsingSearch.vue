<template>
  <div class="map_wrap">
    <div id="map2" style="width:100%; height:100%; position:relative; overflow:hidden;"></div>
    <div id="menu_wrap" class="bg_white">
      <div class="option">
        <form @submit.prevent="createMap">
          키워드 : <input type="text" value="이태원 맛집" id="keyword" size="15" v-model="keyword">
          <button type="submit">검색하기</button>
        </form>
      </div>
      <hr>
      <ul id="placesList"></ul>
      <div id="pagination"></div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      initLatitude: 33.450701, // 기본 위도 값(제주도 Kakao)
      initLongitude: 126.570667, // 기본 경도 값(제주도 Kakao)
      keyword: '',
      markers: [],
      mapContainer: '',
      mapOptions: '',
      map: '',
      ps: '',
      infowindow: '',
      dataArray: '',
      addScriptStatus: false
    }
  },
  created() {
    this.getLocation();
  },
  mounted() {
    this.addScript();
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
    createMap() {
      // map 관련 기본 세팅
      this.mapContainer = document.getElementById('map2');
      this.mapOptions = {
        center: new kakao.maps.LatLng(this.initLatitude, this.initLongitude),
        level: 3
      };
      this.map = new kakao.maps.Map(this.mapContainer, this.mapOptions);
      this.ps = new kakao.maps.services.Places();
      this.infowindow = new kakao.maps.InfoWindow({
        zIndex: 1
      });
      // 키워드 검색
      if (!this.keyword.replace(/^\s+|\s+$/g, '')) {
        if (this.addScriptStatus) {
          // 키워드를 입력하지 않은 경우 현재 내 위치로 이동
          alert('키워드를 입력해주세요');
        }
        return false;
      }
      this.addScriptStatus = true;
      this.ps.keywordSearch(this.keyword, this.placesSearchCB);
    },
    placesSearchCB(data, status, pagination) {
      if (status === kakao.maps.services.Status.OK) {
				// 정상적으로 검색이 완료됐으면
				// 검색 목록과 마커를 표출합니다
				this.displayPlaces(data);
				// 페이지 번호를 표출합니다
				this.displayPagination(pagination);
			} else if (status === kakao.maps.services.Status.ZERO_RESULT) {
        alert('검색 결과가 존재하지 않습니다.');
				return;
			} else if (status === kakao.maps.services.Status.ERROR) {
        alert('검색 결과 중 오류가 발생했습니다.');
				return;
			}
    },
    // 검색 결과 목록과 마커를 표출하는 함수입니다
		displayPlaces(places) {
			let listEl = document.getElementById('placesList');
			let	menuEl = document.getElementById('menu_wrap');
			let	fragment = document.createDocumentFragment();
			let	bounds = new kakao.maps.LatLngBounds();
			// 검색 결과 목록에 추가된 항목들을 제거합니다
			this.removeAllChildNods(listEl);
			// 지도에 표시되고 있는 마커를 제거합니다
			this.removeMarker();
			for (let i = 0; i < places.length; i++) {
				// 마커를 생성하고 지도에 표시합니다
				let placePosition = new kakao.maps.LatLng(places[i].y, places[i].x),
					marker = this.addMarker(placePosition, i),
					itemEl = this.getListItem(i, places[i]); // 검색 결과 항목 Element를 생성합니다
				// 검색된 장소 위치를 기준으로 지도 범위를 재설정하기위해
				// LatLngBounds 객체에 좌표를 추가합니다
				bounds.extend(placePosition);
				// 마커와 검색결과 항목에 mouseover 했을때
				// 해당 장소에 인포윈도우에 장소명을 표시합니다
				// mouseout 했을 때는 인포윈도우를 닫습니다
				((marker, title) => {
					kakao.maps.event.addListener(marker, 'mouseover', () => {
						this.displayInfowindow(marker, title);
					});
					kakao.maps.event.addListener(marker, 'mouseout', () => {
						this.infowindow.close();
					});
					itemEl.onmouseover = () => {
						this.displayInfowindow(marker, title);
					};
					itemEl.onmouseout = () => {
						this.infowindow.close();
					};
				})(marker, places[i].place_name);
				fragment.appendChild(itemEl);
			}
			// 검색결과 항목들을 검색결과 목록 Elemnet에 추가합니다
			listEl.appendChild(fragment);
			menuEl.scrollTop = 0;
			// 검색된 장소 위치를 기준으로 지도 범위를 재설정합니다
			this.map.setBounds(bounds);
    },
    getListItem(index, places) {
      let el = document.createElement('li');
      let itemStr = `
        <span class="markerbg marker_${index + 1}"></span>
        <div class="info">
          <h5>${places.place_name}</h5>
      `;
			if (places.road_address_name) {
        itemStr += `
          <span>${places.road_address_name}</span>
          <span class="jibun gray">${places.address_name}</span>
        `;
			} else {
        itemStr += `
          <span>${places.address_name}</span>
        `;
			}
      itemStr += `
        <span class="tel">${places.phone}</span>
        </div>
      `;
			el.innerHTML = itemStr;
			el.className = 'item';
			return el;
    },
    // 마커를 생성하고 지도 위에 마커를 표시하는 함수입니다
		addMarker(position, idx) {
			let imageSrc = 'http://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_number_blue.png'; // 마커 이미지 url, 스프라이트 이미지를 씁니다
			let	imageSize = new kakao.maps.Size(36, 37); // 마커 이미지의 크기
			let	imgOptions = {
        spriteSize: new kakao.maps.Size(36, 691), // 스프라이트 이미지의 크기
        spriteOrigin: new kakao.maps.Point(0, (idx * 46) + 10), // 스프라이트 이미지 중 사용할 영역의 좌상단 좌표
        offset: new kakao.maps.Point(13, 37) // 마커 좌표에 일치시킬 이미지 내에서의 좌표
      };
			let	markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize, imgOptions);
			let	marker = new kakao.maps.Marker({
        position: position, // 마커의 위치
        image: markerImage,
        clickable: true,
      });
			marker.setMap(this.map); // 지도 위에 마커를 표출합니다
			this.markers.push(marker); // 배열에 생성된 마커를 추가합니다
			return marker;
    },
    removeMarker() {
			for (let i = 0; i < this.markers.length; i++) {
				this.markers[i].setMap(null);
			}
			this.markers = [];
    },
    // 검색결과 목록 하단에 페이지번호를 표시는 함수입니다
		displayPagination(pagination) {
			let paginationEl = document.getElementById('pagination');
			let fragment = document.createDocumentFragment();
			// 기존에 추가된 페이지번호를 삭제합니다
			while (paginationEl.hasChildNodes()) {
				paginationEl.removeChild(paginationEl.lastChild);
			}
			for (let i = 1; i <= pagination.last; i++) {
				let el = document.createElement('a');
				el.href = "#";
				el.innerHTML = i;
				if (i === pagination.current) {
					el.className = 'on';
				} else {
					el.onclick = (function (i) {
						return function () {
							pagination.gotoPage(i);
						}
					})(i);
				}
				fragment.appendChild(el);
			}
			paginationEl.appendChild(fragment);
		},
		// 검색결과 목록 또는 마커를 클릭했을 때 호출되는 함수입니다
		// 인포윈도우에 장소명을 표시합니다
		displayInfowindow(marker, title) {
			let content = `<div style="padding:5px; z-index:1;">${title}</div>`;
			this.infowindow.setContent(content);
			this.infowindow.open(this.map, marker);
		},
		// 검색결과 목록의 자식 Element를 제거하는 함수입니다
		removeAllChildNods(el) {
			while (el.hasChildNodes()) {
				el.removeChild(el.lastChild);
			}
		},
    addScript() {
      const script = document.createElement('script');
      /* global kakao */
      script.onload = () => kakao.maps.load(this.createMap);
      script.src = `http://dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${process.env.VUE_APP_KAKAO_MAP_API_KEY}&libraries=services,clusterer,drawing`;
      document.head.appendChild(script);
    }
  }
}
</script>

<style scoped>
@import './MapUsingSearch.css';
</style>