document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            const target = document.querySelector(this.getAttribute('href'));

            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});

// JavaScript

// Funktion zum Überprüfen, ob ein Element im sichtbaren Bereich ist
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
      rect.top >= 0 &&
      rect.left >= 0 &&
      rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
      rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
  }
  
  // Funktion zum Überprüfen und Einblenden der Mitglieder, wenn sie im sichtbaren Bereich sind
  function checkVisibility() {
    const members = document.querySelectorAll('.body-main-members-container');
    members.forEach(member => {
      if (isInViewport(member)) {
        member.classList.add('visible');
      }
    });
  }
  
  // Event-Listener für das Scroll-Ereignis
  window.addEventListener('scroll', checkVisibility);
  
  // Initialüberprüfung der Sichtbarkeit beim Laden der Seite
  window.addEventListener('DOMContentLoaded', checkVisibility);
  





  function openPopupconection(element) {
    document.getElementById(element).style.display = "block";
    //document.querySelector('.body-header-ul').style.display = 'none'; // Header ausblenden

  }
  
  function closePopup(element) {
    document.getElementById(element).style.display = "none";
    //document.querySelector('.body-header-ul').style.display = 'block'; // Header wieder anzeigen

  }


  /*function adjustConnectionPopupWidth() {
    var connectionPopup = document.getElementById("popup-conection");
    if (connectionPopup) {
      connectionPopup.style.width = "10%";
    }
  }*/