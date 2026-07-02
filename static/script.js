// ==========================
// KONFIRMASI DELETE
// ==========================


function confirmDelete(){

    let confirmAction = confirm(
        "Apakah kamu yakin ingin menghapus data ini?"
    );


    return confirmAction;

}






// ==========================
// CONTACT VALIDATION
// ==========================


function validateContact(){


    let nama =
    document.getElementById("nama").value;


    let email =
    document.getElementById("email").value;


    let pesan =
    document.getElementById("pesan").value;



    if(
        nama === "" ||
        email === "" ||
        pesan === ""
    ){


        alert(
            "Semua form harus diisi!"
        );


        return false;

    }



    alert(
        "Pesan berhasil dikirim"
    );


    return true;


}







// ==========================
// ANIMASI CARD
// ==========================


window.onload=function(){


    let cards =
    document.querySelectorAll(
        ".card, .skill-card"
    );



    cards.forEach(card=>{


        card.style.opacity="0";


        card.style.transform=
        "translateY(20px)";



        setTimeout(()=>{


            card.style.transition=
            "0.5s";


            card.style.opacity="1";


            card.style.transform=
            "translateY(0)";



        },200);



    });



};