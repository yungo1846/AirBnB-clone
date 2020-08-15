module.exports = {
  purge: [],
  theme: {
    extend: {
      spacing: {
        "25vh": "25vh",
        "50vh": "50vh",
        "75vh": "75vh",
      }, // :의 왼쪽은 tailwind의 class name, 오른쪽은 css에게 전달되는 값
      borderRadius: {
        xl: "1.5rem"
      }
    }
  },
  variants: {},
  plugins: [],
}