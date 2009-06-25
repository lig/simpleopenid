var providers = {{ providers|safe }}

function openid_handle_provider() {
	for ( var i = 0; i < providers.length; i++) {
		var provider = providers[i];
		if (provider['pk'] == document.getElementById('id_provider').value) {
			if (provider['fields']['needs_username']) {
				document.getElementById('id_openid_username').type = 'text';
			} else {
				document.getElementById('id_openid_username').type = 'hidden';
			}
		}
	}
}
