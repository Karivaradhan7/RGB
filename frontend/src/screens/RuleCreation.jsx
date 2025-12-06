import React, { useState, useEffect } from 'react'
import { Shield, Plus, Trash2 } from 'lucide-react'
import { createRule, getRules, deleteRule } from '../api'

export default function RuleCreation() {
  const [rules, setRules] = useState([])
  const [formData, setFormData] = useState({
    name: '',
    object_type: 'person',
    threshold: 1,
  })
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    loadRules()
  }, [])

  const loadRules = async () => {
    try {
      const response = await getRules()
      setRules(response.data)
    } catch (error) {
      console.error('Failed to load rules')
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      await createRule(formData.name, formData.object_type, formData.threshold)
      setFormData({ name: '', object_type: 'person', threshold: 1 })
      await loadRules()
    } catch (error) {
      alert('Failed to create rule')
    }
    setLoading(false)
  }

  const handleDeleteRule = async (ruleId) => {
    try {
      await deleteRule(ruleId)
      await loadRules()
    } catch (error) {
      alert('Failed to delete rule')
    }
  }

  return (
    <div className="space-y-8">
      {/* Rule Creation Form */}
      <div className="bg-slate-800/50 backdrop-blur rounded-lg border border-slate-700 p-6">
        <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
          <Shield className="w-6 h-6 text-red-500" />
          Create Detection Rule
        </h2>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Rule Name
              </label>
              <input
                type="text"
                placeholder="e.g., Unauthorized Person Detection"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className="w-full px-4 py-3 bg-slate-900 border border-slate-600 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 transition-colors"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Object Type
              </label>
              <select
                value={formData.object_type}
                onChange={(e) => setFormData({ ...formData, object_type: e.target.value })}
                className="w-full px-4 py-3 bg-slate-900 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500 transition-colors"
              >
                <option value="person">Person</option>
                <option value="animal">Animal</option>
                <option value="vehicle">Vehicle</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Alert Threshold Count
            </label>
            <div className="flex items-center gap-4">
              <input
                type="range"
                min="1"
                max="50"
                value={formData.threshold}
                onChange={(e) => setFormData({ ...formData, threshold: parseInt(e.target.value) })}
                className="flex-1 h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer"
              />
              <div className="bg-blue-600 text-white px-4 py-2 rounded-lg font-bold min-w-16 text-center">
                {formData.threshold}
              </div>
            </div>
            <p className="text-gray-400 text-sm mt-2">
              Alert will trigger when {formData.object_type}s exceed {formData.threshold}
            </p>
          </div>

          <button
            type="submit"
            disabled={loading || !formData.name}
            className="w-full px-6 py-3 bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 disabled:from-slate-600 disabled:to-slate-600 disabled:cursor-not-allowed text-white font-bold rounded-lg transition-all flex items-center justify-center gap-2"
          >
            <Plus className="w-5 h-5" />
            {loading ? 'Creating...' : 'Create Rule'}
          </button>
        </form>
      </div>

      {/* Active Rules */}
      <div className="space-y-4">
        <h3 className="text-xl font-bold text-white">Active Rules ({rules.length})</h3>
        {rules.length === 0 ? (
          <div className="bg-slate-800/50 backdrop-blur rounded-lg border border-dashed border-slate-600 p-12 text-center">
            <p className="text-gray-400">No rules created yet. Create one to get started!</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {rules.map((rule) => (
              <div key={rule.rule_id} className="bg-slate-800/50 backdrop-blur rounded-lg border border-slate-700 p-4 hover:border-slate-600 transition-colors">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex-1">
                    <h4 className="font-bold text-white">{rule.name}</h4>
                    <p className="text-sm text-gray-400 mt-1">
                      {rule.object_type.charAt(0).toUpperCase() + rule.object_type.slice(1)} • Threshold: {rule.threshold}
                    </p>
                  </div>
                  <button
                    onClick={() => handleDeleteRule(rule.rule_id)}
                    className="p-2 hover:bg-red-600/20 rounded-lg text-red-400 transition-colors"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
                <div className="flex items-center gap-2 text-xs">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span className="text-green-400">Active</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
