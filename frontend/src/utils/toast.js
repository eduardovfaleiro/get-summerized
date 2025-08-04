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

const toastTimers = new Map()

export function showToastOncePerInterval(message, interval = 3000) {
  if (toastTimers.has(message)) return

  showToast(message)
  toastTimers.set(message, true)

  setTimeout(() => {
    toastTimers.delete(message)
  }, interval)
}