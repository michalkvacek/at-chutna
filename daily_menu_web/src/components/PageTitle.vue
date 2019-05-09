<script>
    export default {
        name: 'vue-title',
        props: ['title'],
        created() {
            document.title = this.title + " | AťChutná.cz";
        },
        watch: {
            title() {
                document.title = this.title + " | AťChutná.cz";
            }
        },
        render() {
        },
    }
</script>