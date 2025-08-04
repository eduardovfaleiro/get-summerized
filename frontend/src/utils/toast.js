let toastInstance = null

export function registerToast(toast) {
    toastInstance = toast
}

export function showToast(message, options = {}) {
    if (toastInstance) {
        toastInstance.error(message, options)
    } else {
        console.warn('Toast não registrado ainda.')
    }
}