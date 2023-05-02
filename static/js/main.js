function Logout() {
  $.ajax({
    type: "POST",
    url: "/logout", // 보낼 서버의 url
    data: {},
    success: function (response) {
      if (response["result"] == "success") {
        alert("로그아웃 완료");
        window.location.reload();
      } else {
        alert("로그아웃 실패");
        window.location.reload();
      }
    },
  });
}
