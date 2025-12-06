import React, { useState, useEffect } from 'react'
import { Bell, Plus, Trash2, Mail, CheckCircle } from 'lucide-react'
import { configureAlerts, sendTestEmail, getAlerts } from '../api'

export default function AlertSettings() {
  const [emails, setEmails] = useState([])
  const [newEmail, setNewEmail] = useState('')
  const [loading, setLoading] = useState(false)
  const [testLoading, setTestLoading] = useState(false)
  const [successMessage, setSuccessMessage] = useState('')

  const handleAddEmail = () => {
    if (newEmail && !emails.includes(newEmail)) {
      const updatedEmails = [...emails, newEmail]
      setEmails(updatedEmails)
      setNewEmail('')
      saveAlerts(updatedEmails)
    }
  }

  const handleRemoveEmail = (email) => {
    const updatedEmails = emails.filter((e) => e !== email)
    setEmails(updatedEmails)
    saveAlerts(updatedEmails)
  }

  const saveAlerts = async (emailList) => {
    setLoading(true)
    try {
      await configureAlerts(emailList)
    } catch (error) {
      alert('Failed to save alert settings')
    }
    setLoading(false)
  }

  const handleSendTestEmail = async () => {
    if (emails.length === 0) {
      alert('Please add at least one email address')
      return
    }

    setTestLoading(true)
    try {
      await sendTestEmail(emails)
      setSuccessMessage('Test emails sent successfully!')
      setTimeout(() => setSuccessMessage(''), 3000)
    } catch (error) {
      alert('Failed to send test emails')
    }
    setTestLoading(false)
  }

  return (
    <div className="space-y-8">
      {/* Email Configuration */}
      <div className="bg-slate-800/50 backdrop-blur rounded-lg border border-slate-700 p-6">
        <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
          <Bell className="w-6 h-6 text-red-500" />
          Alert Email Settings
        </h2>

        <div className="space-y-6">
          {/* Add Email Form */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-3">
              Add Alert Email Address
            </label>
            <div className="flex gap-3">
              <input
                type="email"
                placeholder="example@email.com"
                value={newEmail}
                onChange={(e) => setNewEmail(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleAddEmail()}
                className="flex-1 px-4 py-3 bg-slate-900 border border-slate-600 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 transition-colors"
              />
              <button
                onClick={handleAddEmail}
                disabled={!newEmail}
                className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-600 disabled:cursor-not-allowed text-white font-medium rounded-lg transition-colors flex items-center gap-2"
              >
                <Plus className="w-4 h-4" />
                Add
              </button>
            </div>
          </div>

          {/* Email List */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-3">
              Configured Emails ({emails.length})
            </label>
            {emails.length === 0 ? (
              <div className="bg-slate-900/50 rounded-lg border border-dashed border-slate-600 p-6 text-center">
                <Mail className="w-8 h-8 text-gray-600 mx-auto mb-2" />
                <p className="text-gray-400">No emails configured yet</p>
              </div>
            ) : (
              <div className="space-y-2">
                {emails.map((email) => (
                  <div
                    key={email}
                    className="flex items-center justify-between bg-slate-900/50 rounded-lg p-4 border border-slate-700 hover:border-slate-600 transition-colors"
                  >
                    <div className="flex items-center gap-3">
                      <Mail className="w-4 h-4 text-blue-400" />
                      <span className="text-white">{email}</span>
                    </div>
                    <button
                      onClick={() => handleRemoveEmail(email)}
                      className="p-2 hover:bg-red-600/20 rounded-lg text-red-400 transition-colors"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Success Message */}
          {successMessage && (
            <div className="bg-green-500/10 border border-green-500/50 rounded-lg p-4 flex items-center gap-3">
              <CheckCircle className="w-5 h-5 text-green-400" />
              <span className="text-green-400">{successMessage}</span>
            </div>
          )}

          {/* Test Email Button */}
          <button
            onClick={handleSendTestEmail}
            disabled={testLoading || emails.length === 0}
            className="w-full px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 disabled:from-slate-600 disabled:to-slate-600 disabled:cursor-not-allowed text-white font-bold rounded-lg transition-all"
          >
            {testLoading ? 'Sending...' : '📧 Send Test Email'}
          </button>
        </div>
      </div>

      {/* Alert Information Card */}
      <div className="bg-gradient-to-r from-blue-900/30 to-cyan-900/30 rounded-lg border border-blue-700/50 p-6">
        <h3 className="text-lg font-bold text-blue-300 mb-3">Alert Email Features</h3>
        <ul className="space-y-2 text-gray-300">
          <li className="flex items-start gap-3">
            <div className="w-2 h-2 bg-blue-400 rounded-full mt-2 flex-shrink-0"></div>
            <span>Alerts are sent immediately when detection rules are triggered</span>
          </li>
          <li className="flex items-start gap-3">
            <div className="w-2 h-2 bg-blue-400 rounded-full mt-2 flex-shrink-0"></div>
            <span>Each email receives rule name, object type, and detection count</span>
          </li>
          <li className="flex items-start gap-3">
            <div className="w-2 h-2 bg-blue-400 rounded-full mt-2 flex-shrink-0"></div>
            <span>Test emails help verify email configuration is working correctly</span>
          </li>
          <li className="flex items-start gap-3">
            <div className="w-2 h-2 bg-blue-400 rounded-full mt-2 flex-shrink-0"></div>
            <span>Add multiple emails to notify different team members</span>
          </li>
        </ul>
      </div>
    </div>
  )
}
