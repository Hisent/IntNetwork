export const mayChangeExperience = (
  confirmBeforeChange: boolean,
  confirmMessage: string,
  confirm: (message: string) => boolean,
) => !confirmBeforeChange || confirm(confirmMessage)
