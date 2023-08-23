const inputButton = document.querySelector("#input");
const imagePreview = document.getElementById("imagePreview");
const imagePreviewContainer = document.getElementById("imagePreviewContainer");
const fileLabel = document.querySelector(".input-label");
const svgDropDown = document.getElementById("svg-drop-down");
const headerDropDown = document.querySelector(".header-submenu")
const headerDropDownMenu = document.querySelector(".header-submenu-li")

inputButton.addEventListener("change", function (event) {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();

    reader.onload = function () {
      imagePreview.src = reader.result;
      imagePreviewContainer.style.display = "block";
    };

    reader.readAsDataURL(file);
  } else {
    // If no image selected, hide the preview container
    inputButton.textContent = "";
    imagePreviewContainer.style.display = "none";
  }
});

svgDropDown.addEventListener("click", () => {
  svgDropDown.classList.toggle("rotated"); // Toggle the "rotated" class

  if (headerDropDown.style.display === "none" || headerDropDown.style.display === "") {
    headerDropDown.style.display = "grid";
  } else {
    headerDropDown.style.display = "none";
  }
  if (headerDropDownMenu.style.display === "none" || headerDropDownMenu.style.display === "") {
    headerDropDownMenu.style.display = "inline-block";
  } else {
    headerDropDownMenu.style.display = "none";
    }
});