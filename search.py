import os
import sublime
import sublime_plugin
import pickle

view_prename = "search files for:"
folderList = []


class OpenFileSearchUnderSelectedCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		if view_prename not in self.view.name():
			return

		sel = self.view.sel()[0]
		if not sel.empty():
			file_name = self.view.substr(sel)
		else:
			caret_pos = self.view.sel()[0].begin()
			current_line = self.view.line(caret_pos)

			left = current_line.begin()
			right = current_line.end()
			file_name = self.vssiew.substr(sublime.Region(left, right))

		print(file_name)
		file_name = file_name.strip()

		if os.path.exists(file_name) and os.path.isfile(file_name):
			self.view.window().open_file(file_name)


class EverythingSearchCommand(sublime_plugin.WindowCommand):

	def run(self):
		self.window.show_input_panel(
			"Folders:", "", None, self.on_change, None)

	def on_change(self, text):
		result = []
		count = 0
		with os.popen("es -n 100 -r " + text) as f:
			for line in f:
				resultItem = {}
				resultItem['caption'] = line

				result.append(resultItem)
				count += 1

		# count = 0w
		# result = f.read()
		# for l in f.readlines():
		#   print(self.decodeText(l))
		#   result += l
		# print(result)

		self.show_quick_panel(result)

	def show_quick_panel(self, items):
		sublime.set_timeout(lambda: self.window.show_quick_panel(items=[
							x["caption"] for x in items], on_select=lambda idx: self.select_item(items, idx)), 10)

	def select_item(self, items, idx):
		# del folderList[:]
		folderList = []
		filePath = items[idx]["caption"]

		# if path dowesn't exist, asks for a custom folder
		print("filepath=" + filePath + "\n")
		dirName = os.path.dirname(filePath)
		print("dirpath=" + dirName + "\n")
		while (os.path.isdir(dirName)):
			folderList.append(dirName)
			nPos = dirName.rfind("\\")
			dirName = dirName[:nPos]

		if (folderList == 0):
			return

		for el in folderList:
			if Folders.exists(self, el):
				folderList.remove(el)

		if (folderList == 0):
			return

		self.window.show_quick_panel(
			folderList, self.on_done, sublime.MONOSPACE_FONT, 0, None)

	def on_done(self, nIndex):
		print(nIndex)
		dirPath = folderList[nIndex]
		global mySelf
		mySelf = self
		AddFolder.add(self, dirPath)
		del folderList[:]


class Folders():

	def add(self, dirPath):
		d = self.window.project_data()

		# if no project present
		if not d:
			d = {'folders': [{'follow_symlinks': True, 'path': dirPath}]}
			self.window.set_project_data(d)
			return

		d['folders'].append({'path': dirPath, 'follow_symlinks': True})
		self.window.set_project_data(d)

	def exists(self, dirPath):
		d = self.window.project_data()
		if d:
			for folder in d['folders']:
				if (folder['path']):
					if os.path.samefile(dirPath, folder['path']):
						return True

		return False

	def remove(self, dirPath):
		d = self.window.project_data()

		nI = 0
		for folder in d['folders']:
			if (folder['path']):
				if os.path.samefile(dirPath, folder['path']):
					del (d['folders'][nI])
					self.window.set_project_data(d)
					return True
				nI = nI + 1
