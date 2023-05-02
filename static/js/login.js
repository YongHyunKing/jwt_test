function Login() {
  const email = document.querySelector(".email").value;
  const password = document.querySelector(".password").value;
  console.log(email);
  console.log(password);
  $.ajax({
    type: "POST",
    url: "/login", // 보낼 서버의 url
    data: {
      give_email: email,
      give_password: password,
    },
    success: function (response) {
      if (response["result"] == "success") {
        alert("로그인 되었습니다");
        window.location.reload();
      } else {
        alert("로그인 실패");
        window.location.reload();
      }
    },
  });
}
