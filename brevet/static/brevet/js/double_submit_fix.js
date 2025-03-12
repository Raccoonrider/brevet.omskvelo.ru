document.querySelectorAll('form').forEach((form) => {
	form.addEventListener('submit', (e) => {
		if (form.classList.contains('is-submitting')) {
			e.preventDefault();
			e.stopPropagation();
			return false;	
		};

		form.classList.add('is-submitting');
	});
});