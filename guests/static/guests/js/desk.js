/* Desk page QR scanner + autocomplete */
(function () {
    const btn          = document.getElementById("btnScan");
    const btnClose     = document.getElementById("btnCloseModal");
    const backdrop     = document.getElementById("qr-backdrop");
    const modal        = document.getElementById("qr-modal");
    const input        = document.querySelector("input[name='query']");
    const acList       = document.getElementById("autocomplete-list");

    // --- Walk-in modal ---
    const btnWalkIn      = document.getElementById("btnWalkIn");
    const walkinModal    = document.getElementById("walkin-modal");
    const walkinBackdrop = document.getElementById("walkin-backdrop");
    const btnCloseWalkIn = document.getElementById("btnCloseWalkIn");

    if (btnWalkIn) {
        btnWalkIn.addEventListener("click", () => {
            walkinModal.classList.remove("hidden");
            document.body.style.overflow = "hidden";
            walkinModal.querySelector("input[name='name']").focus();
        });
    }
    function closeWalkIn() {
        if (walkinModal) {
            walkinModal.classList.add("hidden");
            document.body.style.overflow = "";
        }
    }
    if (btnCloseWalkIn) btnCloseWalkIn.addEventListener("click", closeWalkIn);
    if (walkinBackdrop) walkinBackdrop.addEventListener("click", closeWalkIn);

    if (!btn) return;
  
    let scanner = null;
    let isScanning = false;
    let acTimeout = null;
  
    btn.addEventListener("click", () => startScanner());
    btnClose.addEventListener("click", () => stopScanner());
    backdrop.addEventListener("click", () => stopScanner());
  
    function openModal() {
      modal.classList.remove("hidden");
      document.body.style.overflow = "hidden";
    }

    function closeModal() {
      modal.classList.add("hidden");
      document.body.style.overflow = "";
    }

    function startScanner() {
      openModal();
      isScanning = true;
  
      scanner = new Html5Qrcode("qr-reader");
      scanner.start(
        { facingMode: "environment" },
        { fps: 10, qrbox: { width: 250, height: 250 } },
        (decodedText) => {
          stopScanner();
          input.value = decodedText.trim();
          const submitBtn = document.querySelector('button[type="submit"]');
          if (submitBtn) {
            submitBtn.click();
          } else {
            const form = document.querySelector('form');
            if (form) form.submit();
          }
        },
        (err) => console.debug(err)
      ).catch((err) => {
        console.error("Failed to start scanner:", err);
        stopScanner();
      });
    }
  
    function stopScanner() {
      if (scanner) {
        scanner.stop().then(() => {
          scanner.clear();
          scanner = null;
        }).catch((err) => {
          console.error("Error stopping scanner:", err);
        });
      }
      isScanning = false;
      closeModal();
    }

    // --- Autocomplete logic ---
    if (input && acList) {
      input.setAttribute('autocomplete', 'off');
      input.addEventListener('input', function() {
        const val = this.value.trim();
        if (acTimeout) clearTimeout(acTimeout);
        if (val.length < 2) {
          acList.innerHTML = '';
          acList.classList.add('hidden');
          return;
        }
        acTimeout = setTimeout(() => {
          fetch(`/api/guests/search/?q=${encodeURIComponent(val)}`)
            .then(r => r.json())
            .then(data => {
              acList.innerHTML = '';
              if (data.results && data.results.length > 0) {
                data.results.forEach(g => {
                  const opt = document.createElement('div');
                  opt.className = 'px-4 py-2 cursor-pointer hover:bg-blue-100 flex flex-col text-left';
                  opt.innerHTML = `<span class='font-semibold text-gray-800'>${g.name}</span><span class='text-xs text-gray-500'>${g.invitation_code} &middot; ${g.status}</span>${g.detail ? `<span class='text-xs text-rose-700 italic'>${g.detail}</span>` : ''}`;
                  opt.addEventListener('mousedown', function(e) {
                    e.preventDefault();
                    input.value = g.invitation_code;
                    acList.innerHTML = '';
                    acList.classList.add('hidden');
                  });
                  acList.appendChild(opt);
                });
                acList.classList.remove('hidden');
              } else {
                acList.classList.add('hidden');
              }
            });
        }, 200);
      });
      // Hide dropdown on blur
      input.addEventListener('blur', function() {
        setTimeout(() => {
          acList.innerHTML = '';
          acList.classList.add('hidden');
        }, 150);
      });
    }
})();
  