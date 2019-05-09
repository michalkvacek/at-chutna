<template>
    <v-dialog
            v-model="dialog"
            width="500">
        <template v-slot:activator="{ on }">
            <v-btn v-on="on">
                Proč se tu zobrazují tyto restaurace?
            </v-btn>
        </template>

        <v-card>
            <v-card-title
                    class="headline grey lighten-2"
                    primary-title>
                Proč se tu zobrazují tyto restaurace?
            </v-card-title>

            <v-card-text>
                <p>
                    Tato sekce obsahuje restaurace, ve které jste navštívili v posledních dnech vícekrát, případně ty,
                    jejichž menu jste označili že se vám líbí. Tento seznam se průběžně mění a je generován automaticky.
                </p>
                <p>
                    Pokud chcete přidat nějakou restauraci do nějakého seznamu, ve kterém budete mít rychlejší přístup k
                    jejím menu, stačí využít ikonu hvězdičky v seznamu a restaurace se začně zobrazovat v seznamu
                    <strong>Sledovaných restaurací</strong>.
                </p>
            </v-card-text>

            <v-divider></v-divider>

            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary"
                       flat
                       @click="dialog = false">
                    Díky za info
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
    export default {
        name: "favourite-restaurants-help",
        data() {
            return {
                dialog: false
            }
        }
    }
</script>